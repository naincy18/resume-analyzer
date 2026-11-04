from datetime import datetime

from pydantic import BaseModel, Field


# ---------- Upload (unchanged) ----------
class UploadResponse(BaseModel):
    resume_id: int
    filename: str
    page_count: int
    text_length: int
    text_preview: str
    message: str


# ---------- Analysis (NEW) ----------
class AnalyzeRequest(BaseModel):
    """What the frontend sends to POST /api/analyze."""
    resume_id: int
    job_description: str = Field(min_length=20, max_length=10000)


class AnalysisResponse(BaseModel):
    """What POST /api/analyze and GET /api/analysis/{id} both return."""
    id: int
    resume_id: int
    match_score: float
    semantic_similarity: float | None = None
    matched_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class HistoryItem(BaseModel):
    """One row in GET /api/history (a short summary, not the full result)."""
    id: int
    resume_id: int
    filename: str
    match_score: float
    created_at: datetime