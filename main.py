


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

# # =====================================================================
# # ENDPOINT 1: WORD TO PDF (Kept exactly as you had it)
# # =====================================================================
# @app.post("/convert/word-to-pdf")
# async def word_to_pdf(file: UploadFile = File(...)):
#     if not file.filename.endswith(('.docx', '.doc')):
#         raise HTTPException(status_code=400, detail="Only .docx and .doc files are supported")
#     tmp_dir = tempfile.mkdtemp()
#     try:
#         input_path = os.path.join(tmp_dir, file.filename)
#         with open(input_path, "wb") as f:
#             content = await file.read()
#             f.write(content)
#         result = subprocess.run([
#             "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", tmp_dir, input_path
#         ], capture_output=True, text=True, timeout=60)
#         if result.returncode != 0:
#             raise HTTPException(status_code=500, detail=f"Conversion failed: {result.stderr}")
#         pdf_filename = os.path.splitext(file.filename)[0] + ".pdf"
#         pdf_path = os.path.join(tmp_dir, pdf_filename)
#         if not os.path.exists(pdf_path):
#             raise HTTPException(status_code=500, detail="PDF was not created")
#         with open(pdf_path, "rb") as f:
#             pdf_bytes = f.read()
#         return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{pdf_filename}"'})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         shutil.rmtree(tmp_dir, ignore_errors=True)


# # =====================================================================
# # ENDPOINT 2: PDF TO WORD (DIAGNOSTIC SYSTEM)
# # =====================================================================
# @app.post("/convert/pdf-to-word")
# async def pdf_to_word(file: UploadFile = File(...)):
#     if not file.filename.endswith('.pdf'):
#         raise HTTPException(status_code=400, detail="Only .pdf files are supported")

#     # TEST FLAG: If you see this exact error in Postman, the deploy succeeded!
#     # If you still see "500: DOCX was not created", Railway is definitively serving old code.
#     try:
#         from pdf2docx import Converter
#     except ImportError as import_err:
#         raise HTTPException(
#             status_code=500, 
#             detail=f"[DIAGNOSTIC-ACTIVE] Code updated, but pdf2docx library is missing in your requirements file: {str(import_err)}"
#         )

#     tmp_dir = tempfile.mkdtemp()
#     try:
#         input_path = os.path.join(tmp_dir, file.filename)
#         with open(input_path, "wb") as f:
#             content = await file.read()
#             f.write(content)

#         docx_filename = os.path.splitext(file.filename)[0] + ".docx"
#         docx_path = os.path.join(tmp_dir, docx_filename)

#         # Run conversion
#         cv = Converter(input_path)
#         cv.convert(docx_path, start=0, end=None)
#         cv.close()

#         if not os.path.exists(docx_path):
#             raise HTTPException(
#                 status_code=500,
#                 detail="[DIAGNOSTIC-ACTIVE] Conversion completed but system could not locate output file."
#             )

#         with open(docx_path, "rb") as f:
#             docx_bytes = f.read()

#         return Response(
#             content=docx_bytes,
#             media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#             headers={"Content-Disposition": f'attachment; filename="{docx_filename}"'}
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"[DIAGNOSTIC-ACTIVE] Engine crash: {str(e)}")
#     finally:
#         shutil.rmtree(tmp_dir, ignore_errors=True)


# // server.js (Node.js / Express + ghostscript must be installed on Railway)
# app.post('/convert/compress-pdf', upload.single('file'), async (req, res) => {
#   const quality = parseInt(req.body.quality ?? '70');

#   // Map quality (0-100) to Ghostscript preset
#   let gsPreset;
#   if (quality >= 75)      gsPreset = 'printer';   // ~300 dpi
#   else if (quality >= 45) gsPreset = 'ebook';     // ~150 dpi  
#   else if (quality >= 20) gsPreset = 'screen';    // ~72 dpi
#   else                    gsPreset = 'screen';

#   const inputPath  = req.file.path;
#   const outputPath = inputPath + '_compressed.pdf';

#   try {
#     await execPromise(
#       `gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
#           -dPDFSETTINGS=/${gsPreset} \
#           -dNOPAUSE -dQUIET -dBATCH \
#           -sOutputFile="${outputPath}" "${inputPath}"`
#     );
#     res.download(outputPath, 'compressed.pdf', () => {
#       fs.unlinkSync(inputPath);
#       fs.unlinkSync(outputPath);
#     });
#   } catch (err) {
#     res.status(500).json({ error: err.message });
#   }
# });

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
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
# ENDPOINT 1: WORD TO PDF
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
        return Response(content=pdf_bytes, media_type="application/pdf",
                        headers={"Content-Disposition": f'attachment; filename="{pdf_filename}"'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# =====================================================================
# ENDPOINT 2: PDF TO WORD
# =====================================================================
@app.post("/convert/pdf-to-word")
async def pdf_to_word(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only .pdf files are supported")
    try:
        from pdf2docx import Converter
    except ImportError as import_err:
        raise HTTPException(
            status_code=500,
            detail=f"[DIAGNOSTIC-ACTIVE] pdf2docx library missing: {str(import_err)}"
        )
    tmp_dir = tempfile.mkdtemp()
    try:
        input_path = os.path.join(tmp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        docx_filename = os.path.splitext(file.filename)[0] + ".docx"
        docx_path = os.path.join(tmp_dir, docx_filename)
        cv = Converter(input_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
        if not os.path.exists(docx_path):
            raise HTTPException(status_code=500, detail="Conversion completed but output file not found.")
        with open(docx_path, "rb") as f:
            docx_bytes = f.read()
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{docx_filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine crash: {str(e)}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# =====================================================================
# ENDPOINT 3: COMPRESS PDF (Ghostscript)
# =====================================================================
@app.post("/convert/compress-pdf")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: int = Form(70),
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only .pdf files are supported")

    # Map quality (0–100) to Ghostscript PDFSETTINGS preset
    # /screen  → ~72  dpi  — smallest file, lowest quality
    # /ebook   → ~150 dpi  — good for reading on screen
    # /printer → ~300 dpi  — high quality, moderate compression
    # /prepress→ ~300 dpi  — maximum quality, least compression
    if quality >= 75:
        gs_preset = "printer"
    elif quality >= 45:
        gs_preset = "ebook"
    else:
        gs_preset = "screen"

    tmp_dir = tempfile.mkdtemp()
    try:
        input_path = os.path.join(tmp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)

        original_size = os.path.getsize(input_path)

        output_filename = "compressed_" + file.filename
        output_path = os.path.join(tmp_dir, output_filename)

        result = subprocess.run([
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{gs_preset}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            input_path,
        ], capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Ghostscript error: {result.stderr}"
            )

        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Compressed PDF was not created")

        compressed_size = os.path.getsize(output_path)

        # If Ghostscript made it larger (e.g. already-optimised PDF),
        # return the original so the client never gets a bigger file.
        if compressed_size >= original_size:
            with open(input_path, "rb") as f:
                pdf_bytes = f.read()
        else:
            with open(output_path, "rb") as f:
                pdf_bytes = f.read()

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{output_filename}"'}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)