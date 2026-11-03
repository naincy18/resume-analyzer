
from fastapi import APIRouter, File, UploadFile, status

from models.schemas import UploadResponse
from services.file_validation import read_and_validate_pdf
from services.pdf_parser import extract_text_from_pdf

router = APIRouter(prefix="/api/resume", tags=["Resume"])

PREVIEW_LENGTH = 300


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(file: UploadFile = File(...)):
    # Step 1: Validate the uploaded PDF
    filename, content = await read_and_validate_pdf(file)

    # Step 2: Extract text from the PDF
    text, page_count = extract_text_from_pdf(content)

    # Step 3: Return the response
    return UploadResponse(
        filename=filename,
        page_count=page_count,
        text_length=len(text),
        text_preview=text[:PREVIEW_LENGTH],
        message="Resume uploaded and text extracted successfully.",
    )
