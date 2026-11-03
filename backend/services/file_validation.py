from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from config import settings

ALLOWED_EXTENSION = ".pdf"
CHUNK_SIZE = 1024 * 1024  # read the file 1 MB at a time

# Every real PDF starts with these 5 bytes
PDF_SIGNATURE = b"%PDF-"


async def read_and_validate_pdf(file: UploadFile) -> tuple[str, bytes]:
    """Validate an uploaded file and return (filename, file_bytes).

    Raises HTTPException with a clear message if the file is not acceptable.
    """

    # 1. The upload must have a filename.
    #    Path(...).name removes any folder parts, so "../../evil.pdf" becomes "evil.pdf".
    if not file.filename:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No file name provided.")
    filename = Path(file.filename).name

    # 2. Only .pdf files are allowed.
    if Path(filename).suffix.lower() != ALLOWED_EXTENSION:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Only PDF files are allowed.",
        )

    # 3. Read the file in chunks. Stop as soon as it passes the size limit,
    #    so a huge upload cannot fill up the server's memory.
    data = bytearray()
    while chunk := await file.read(CHUNK_SIZE):
        data.extend(chunk)
        if len(data) > settings.max_upload_size_bytes:
            raise HTTPException(
                status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                f"File is too large. Maximum size is {settings.max_upload_size_mb} MB.",
            )

    # 4. Reject empty files.
    if len(data) == 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The uploaded file is empty.")

    # 5. Check the file's real content. Anyone can rename a .txt file to .pdf,
    #    but the first bytes of a real PDF are always "%PDF-".
    content = bytes(data)
    if not content.startswith(PDF_SIGNATURE):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This is not a valid PDF file.")

    return filename, content