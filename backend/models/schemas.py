from pydantic import BaseModel


class UploadResponse(BaseModel):
    resume_id: int
    filename: str
    page_count: int
    text_length: int
    text_preview: str
    message: str