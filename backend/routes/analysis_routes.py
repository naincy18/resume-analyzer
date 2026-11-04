from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import get_db
from ml_engine import analyze_resume  # stub now, real AI module later
from models.db_models import Analysis, Resume
from models.schemas import AnalysisResponse, AnalyzeRequest, HistoryItem

router = APIRouter(prefix="/api", tags=["Analysis"])

HISTORY_LIMIT = 50


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)):
    # 1. The resume must exist in the database.
    resume = db.get(Resume, request.resume_id)
    if resume is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resume not found.")

    # 2. Call the AI module. All AI logic stays inside analyze_resume.
    try:
        result = analyze_resume(resume.extracted_text, request.job_description)
        match_score = float(result["match_score"])
        similarity = result.get("semantic_similarity")
        similarity = float(similarity) if similarity is not None else None
        matched_skills = list(result["matched_skills"])
        missing_skills = list(result["missing_skills"])
        suggestions = list(result["suggestions"])
    except Exception:
        # Generic message: never leak resume text or internal errors.
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "The analysis engine failed. Please try again.",
        )

    # 3. Save the result.
    analysis = Analysis(
        resume_id=resume.id,
        job_description=request.job_description,
        match_score=match_score,
        semantic_similarity=similarity,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        suggestions=suggestions,
    )
    try:
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Could not save the analysis. Please try again.",
        )

    return analysis


@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.get(Analysis, analysis_id)
    if analysis is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Analysis not found.")
    return analysis


@router.get("/history", response_model=list[HistoryItem])
def get_history(db: Session = Depends(get_db)):
    # Join analyses with resumes so each row can show the filename.
    rows = db.execute(
        select(Analysis, Resume.filename)
        .join(Resume, Analysis.resume_id == Resume.id)
        .order_by(Analysis.created_at.desc())
        .limit(HISTORY_LIMIT)
    ).all()

    return [
        HistoryItem(
            id=a.id,
            resume_id=a.resume_id,
            filename=filename,
            match_score=a.match_score,
            created_at=a.created_at,
        )
        for a, filename in rows
    ]