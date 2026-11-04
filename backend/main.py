import logging  # NEW

from fastapi import FastAPI, Request  # NEW: Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # NEW

from config import settings
from routes.resume_routes import router as resume_router
from routes.analysis_routes import router as analysis_router

# NEW: basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("resume_analyzer")

app = FastAPI(
    title=settings.app_name,
    description="Backend for the AI-Powered Resume Analyzer",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(analysis_router)


# NEW: catches any error we did not handle ourselves
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Log only the route and the error TYPE. The error message is skipped on
    # purpose, because it could contain resume text or other personal data.
    logger.error(
        "Unhandled error on %s %s: %s",
        request.method,
        request.url.path,
        type(exc).__name__,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong on the server. Please try again."},
    )


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": settings.app_name}



