from pathlib import Path
from uuid import uuid4
import hashlib, logging
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import Document, User
from app.security import get_current_user
from document_processing.extractor import extract_text
from document_processing.classifier import classify_document
from document_processing.validator import validate_file

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/documents", tags=["Documents"])
ALLOWED = {".pdf", ".csv", ".txt", ".docx"}
MAX_BYTES = 10 * 1024 * 1024

@router.post("/upload", status_code=201)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    original = Path(file.filename or "upload").name
    ext = Path(original).suffix.lower()
    if ext not in ALLOWED: raise HTTPException(415, "Only PDF, CSV, TXT and DOCX files are allowed")
    content = await file.read(MAX_BYTES + 1)
    try:
        validate_file(original, len(content), MAX_BYTES)
    except ValueError as exc:
        raise HTTPException(413 if len(content) > MAX_BYTES else 400, str(exc))
    digest = hashlib.sha256(content).hexdigest()
    if db.query(Document).filter(Document.sha256 == digest).first():
        raise HTTPException(409, "Duplicate document detected (same file content)")
    try:
        extracted = extract_text(content, ext)
    except Exception as exc:
        logger.exception("Document extraction failed")
        raise HTTPException(422, f"Could not process document: {exc}")
    stored = f"{uuid4().hex}{ext}"
    folder = Path(settings.upload_dir); folder.mkdir(parents=True, exist_ok=True)
    target = folder / stored
    target.write_bytes(content)
    item = Document(original_name=original, stored_name=stored, extension=ext, size_bytes=len(content),
                    sha256=digest, category=classify_document(original, extracted),
                    extracted_text=extracted[:100000], uploaded_by=user.id)
    try:
        db.add(item); db.commit(); db.refresh(item)
    except Exception:
        db.rollback()
        target.unlink(missing_ok=True)
        raise
    logger.info("Document uploaded id=%s filename=%s", item.id, original)
    return {"id": item.id, "filename": item.original_name, "category": item.category,
            "size_bytes": item.size_bytes, "sha256": item.sha256, "extracted_characters": len(extracted)}

@router.get("")
def list_documents(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Document).order_by(Document.id.desc()).all()
