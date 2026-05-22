# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.responses import Response
# import subprocess
# import tempfile
# import os
# import shutil

# app = FastAPI()

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.post("/convert/word-to-pdf")
# async def word_to_pdf(file: UploadFile = File(...)):
#     if not file.filename.endswith(('.docx', '.doc')):
#         raise HTTPException(
#             status_code=400,
#             detail="Only .docx and .doc files are supported"
#         )

#     tmp_dir = tempfile.mkdtemp()
#     try:
#         input_path = os.path.join(tmp_dir, file.filename)
#         with open(input_path, "wb") as f:
#             content = await file.read()
#             f.write(content)

#         result = subprocess.run([
#             "libreoffice",
#             "--headless",
#             "--convert-to", "pdf",
#             "--outdir", tmp_dir,
#             input_path
#         ], capture_output=True, text=True, timeout=60)

#         if result.returncode != 0:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Conversion failed: {result.stderr}"
#             )

#         pdf_filename = os.path.splitext(file.filename)[0] + ".pdf"
#         pdf_path = os.path.join(tmp_dir, pdf_filename)

#         if not os.path.exists(pdf_path):
#             raise HTTPException(
#                 status_code=500,
#                 detail="PDF was not created"
#             )

#         with open(pdf_path, "rb") as f:
#             pdf_bytes = f.read()

#         return Response(
#             content=pdf_bytes,
#             media_type="application/pdf",
#             headers={
#                 "Content-Disposition": f'attachment; filename="{pdf_filename}"'
#             }
#         )

#     except subprocess.TimeoutExpired:
#         raise HTTPException(status_code=408, detail="Conversion timed out")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         shutil.rmtree(tmp_dir, ignore_errors=True)


# @app.post("/convert/pdf-to-word")
# async def pdf_to_word(file: UploadFile = File(...)):
#     if not file.filename.endswith('.pdf'):
#         raise HTTPException(
#             status_code=400,
#             detail="Only .pdf files are supported"
#         )

#     tmp_dir = tempfile.mkdtemp()
#     try:
#         input_path = os.path.join(tmp_dir, file.filename)
#         with open(input_path, "wb") as f:
#             content = await file.read()
#             f.write(content)

#         result = subprocess.run([
#             "libreoffice",
#             "--headless",
#             "--convert-to", "docx:MS Word 2007 XML",
#             "--outdir", tmp_dir,
#             input_path
#         ], capture_output=True, text=True, timeout=60)

#         if result.returncode != 0:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Conversion failed: {result.stderr}"
#             )

#         docx_filename = os.path.splitext(file.filename)[0] + ".docx"
#         docx_path = os.path.join(tmp_dir, docx_filename)

#         if not os.path.exists(docx_path):
#             raise HTTPException(
#                 status_code=500,
#                 detail="DOCX was not created"
#             )

#         with open(docx_path, "rb") as f:
#             docx_bytes = f.read()

#         return Response(
#             content=docx_bytes,
#             media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#             headers={
#                 "Content-Disposition": f'attachment; filename="{docx_filename}"'
#             }
#         )

#     except subprocess.TimeoutExpired:
#         raise HTTPException(status_code=408, detail="Conversion timed out")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         shutil.rmtree(tmp_dir, ignore_errors=True)


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
import subprocess
import tempfile
import os
import shutil
# 1. Added the new python package needed for stable PDF-to-Word conversion
from pdf2docx import Converter

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


# =====================================================================
# ENDPOINT 1: WORD TO PDF (Kept exactly as you had it)
# =====================================================================
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


# =====================================================================
# ENDPOINT 2: PDF TO WORD (UPDATED & FIXED)
# =====================================================================
@app.post("/convert/pdf-to-word")
async def pdf_to_word(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only .pdf files are supported"
        )

    tmp_dir = tempfile.mkdtemp()
    try:
        # Step A: Save incoming PDF into temporary directory
        input_path = os.path.join(tmp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Step B: Set up output filename and path (.docx)
        docx_filename = os.path.splitext(file.filename)[0] + ".docx"
        docx_path = os.path.join(tmp_dir, docx_filename)

        # Step C: Use pdf2docx to cleanly rebuild the layout instead of LibreOffice
        cv = Converter(input_path)
        cv.convert(docx_path, start=0, end=None)  # Converts all pages
        cv.close()

        # Step D: Make sure it was built successfully
        if not os.path.exists(docx_path):
            raise HTTPException(
                status_code=500,
                detail="DOCX was not created"
            )

        # Step E: Read the generated Word bytes
        with open(docx_path, "rb") as f:
            docx_bytes = f.read()

        # Step F: Stream file back down to Postman/Flutter
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f'attachment; filename="{docx_filename}"'
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Step G: Clean up the temporary folder entirely to keep Railway lightweight
        shutil.rmtree(tmp_dir, ignore_errors=True)