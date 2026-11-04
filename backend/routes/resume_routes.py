from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status  # NEW: Depends
from sqlalchemy.exc import SQLAlchemyError  # NEW
from sqlalchemy.orm import Session  # NEW

from database import get_db  # NEW
from models.db_models import Resume  # NEW
from models.schemas import UploadResponse
from services.file_validation import read_and_validate_pdf
from services.pdf_parser import extract_text_from_pdf

router = APIRouter(prefix="/api/resume", tags=["Resume"])

PREVIEW_LENGTH = 300  # how many characters of text to show in the response


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),  # NEW: a database session for this request
):
    # Step 1: validate the file (extension, size, empty, real PDF)
    filename, content = await read_and_validate_pdf(file)

    # Step 2: extract the text with PyMuPDF
    text, page_count = extract_text_from_pdf(content)

    # Step 3 (NEW): save the resume to PostgreSQL
    resume = Resume(filename=filename, extracted_text=text)
    try:
        db.add(resume)      # stage the new row
        db.commit()         # write it to the database
        db.refresh(resume)  # reload it so we get the generated id
    except SQLAlchemyError:
        db.rollback()       # undo the failed save
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Could not save the resume. Please try again.",
        )

    # Step 4: build the response
    return UploadResponse(
        resume_id=resume.id,  # NEW
        filename=filename,
        page_count=page_count,
        text_length=len(text),
        text_preview=text[:PREVIEW_LENGTH],
        message="Resume uploaded and saved successfully.",
    )
