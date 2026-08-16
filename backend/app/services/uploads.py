from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
ALLOWED_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".txt", ".doc", ".docx"}
MAX_BYTES = 5 * 1024 * 1024


def ensure_upload_dir() -> None:
    """Create the assignment-upload folder on startup."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_submission_file(assignment_id: int, student_id: int, upload: UploadFile) -> tuple[str, str]:
    original = Path(upload.filename or "attachment").name
    suffix = Path(original).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Allowed attachments: PDF, PNG, JPG, TXT, DOC, DOCX",
        )
    data = upload.file.read()
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be 5 MB or smaller")

    folder = UPLOAD_DIR / str(assignment_id)
    folder.mkdir(parents=True, exist_ok=True)
    stored_name = f"{student_id}_{uuid4().hex}{suffix}"
    dest = folder / stored_name
    dest.write_bytes(data)
    relative = f"{assignment_id}/{stored_name}"
    return relative, original


def resolve_upload(relative: str) -> Path:
    path = (UPLOAD_DIR / relative).resolve()
    if not str(path).startswith(str(UPLOAD_DIR.resolve())) or not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return path
