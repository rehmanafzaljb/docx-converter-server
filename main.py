from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
import subprocess
import tempfile
import os
import shutil

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/convert/word-to-pdf")
async def word_to_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(('.docx', '.doc')):
        raise HTTPException(
            status_code=400,
            detail="Only .docx and .doc files are supported"
        )

    tmp_dir = tempfile.mkdtemp()
    try:
        input_path = os.path.join(tmp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)

        result = subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", tmp_dir,
            input_path
        ], capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Conversion failed: {result.stderr}"
            )

        pdf_filename = os.path.splitext(file.filename)[0] + ".pdf"
        pdf_path = os.path.join(tmp_dir, pdf_filename)

        if not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=500,
                detail="PDF was not created"
            )

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{pdf_filename}"'
            }
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Conversion timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)