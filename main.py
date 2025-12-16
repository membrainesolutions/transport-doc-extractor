from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from pypdf import PdfReader
import io

app = FastAPI(title="Transport PDF Extractor")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/extract/text")
async def extract_text(
    file: UploadFile = File(...),
    page: int = Query(1, ge=1)
):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        reader = PdfReader(io.BytesIO(data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if page > len(reader.pages):
        raise HTTPException(status_code=400, detail="Page out of range")

    text = reader.pages[page - 1].extract_text() or ""

    return {
        "page": page,
        "hasText": len(text.strip()) > 20,
        "text": text.strip()
    }
