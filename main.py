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
        raise HTTPException(status_code=400, detail="Only .docx and .doc files are supported")
    tmp_dir = tempfile.mkdtemp()
    try:
        input_path = os.path.join(tmp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        result = subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", tmp_dir, input_path
        ], capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Conversion failed: {result.stderr}")
        pdf_filename = os.path.splitext(file.filename)[0] + ".pdf"
        pdf_path = os.path.join(tmp_dir, pdf_filename)
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="PDF was not created")
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{pdf_filename}"'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# =====================================================================
# ENDPOINT 2: PDF TO WORD (DIAGNOSTIC SYSTEM)
# =====================================================================
@app.post("/convert/pdf-to-word")
async def pdf_to_word(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only .pdf files are supported")

    # TEST FLAG: If you see this exact error in Postman, the deploy succeeded!
    # If you still see "500: DOCX was not created", Railway is definitively serving old code.
    try:
        from pdf2docx import Converter
    except ImportError as import_err:
        raise HTTPException(
            status_code=500, 
            detail=f"[DIAGNOSTIC-ACTIVE] Code updated, but pdf2docx library is missing in your requirements file: {str(import_err)}"
        )

    tmp_dir = tempfile.mkdtemp()
    try:
        input_path = os.path.join(tmp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)

        docx_filename = os.path.splitext(file.filename)[0] + ".docx"
        docx_path = os.path.join(tmp_dir, docx_filename)

        # Run conversion
        cv = Converter(input_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()

        if not os.path.exists(docx_path):
            raise HTTPException(
                status_code=500,
                detail="[DIAGNOSTIC-ACTIVE] Conversion completed but system could not locate output file."
            )

        with open(docx_path, "rb") as f:
            docx_bytes = f.read()

        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{docx_filename}"'}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[DIAGNOSTIC-ACTIVE] Engine crash: {str(e)}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)