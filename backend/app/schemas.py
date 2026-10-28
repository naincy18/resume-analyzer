from pydantic import BaseModel
from typing import Literal

class SkillsResult(BaseModel):
    matched: list[str]
    missing: list[str]

class Suggestion(BaseModel):
    original: str
    improved: str
    reason: str

class AtsIssue(BaseModel):
    severity: Literal["high", "medium", "low"]
    message: str

class ScoreBreakdown(BaseModel):
    skills: float
    experience: float
    education: float
    keywords: float

class AnalyzeResponse(BaseModel):
    match_score: float              # 0-100
    scorer: str                     # "tfidf" | "embeddings"
    breakdown: ScoreBreakdown
    skills: SkillsResult
    suggestions: list[Suggestion]
    ats_issues: list[AtsIssue]