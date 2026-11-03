from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes.resume_routes import router as resume_router

app = FastAPI(
    title=settings.app_name,
    description="Backend for the AI-Powered Resume Analyzer",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register resume routes
app.include_router(resume_router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": settings.app_name}

