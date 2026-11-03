import re

import pymupdf  # PyMuPDF
from fastapi import HTTPException, status

MAX_PAGES = 20  # a resume should never be longer than this


def extract_text_from_pdf(content: bytes) -> tuple[str, int]:
    """Extract readable text from PDF bytes.

    Returns (text, page_count).
    Raises HTTPException if the PDF is broken, locked, too long, or has no text.
    """

    # 1. Open the PDF from memory. If the file is corrupted, PyMuPDF raises
    #    an error, and we turn it into a clean message for the client.
    try:
        doc = pymupdf.open(stream=content, filetype="pdf")
    except Exception:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "The PDF file is corrupted or cannot be read.",
        )

    # "with" makes sure the document is always closed, even if an error happens.
    with doc:
        # 2. Password-protected PDFs cannot be read.
        if doc.needs_pass:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "The PDF is password-protected. Please upload an unlocked file.",
            )

        # 3. Reject very long documents.
        page_count = doc.page_count
        if page_count > MAX_PAGES:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"The PDF has too many pages. Maximum is {MAX_PAGES}.",
            )

        # 4. Read the text of every page.
        try:
            pages = [page.get_text("text") for page in doc]
        except Exception:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Could not read text from this PDF.",
            )

    # 5. Clean the text: join pages, then shrink many blank lines to one.
    text = "\n".join(pages)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # 6. A scanned PDF is just images, so it has no text to extract.
    #    OCR support will be a future enhancement.
    if not text:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "No readable text found. This looks like a scanned PDF. "
            "Please upload a PDF with selectable text.",
        )

    return text, page_count