# AI-Powered Resume Analyzer

A web app that analyzes a resume against a job description. Upload a PDF resume, paste a job description, and get a match score, matched and missing skills, and suggestions for improvement.

## Features

- Upload PDF resumes with validation and text extraction
- Match score and semantic similarity against a job description
- Matched vs. missing skills
- Improvement suggestions
- Saved analysis history

## Tech Stack


Frontend | React.js |
Backend | Python, FastAPI, SQLAlchemy |
Database | PostgreSQL |
AI/ML | NLP, TF-IDF, sentence embeddings |
PDF parsing | PyMuPDF |

## How It Works

```
React frontend  →  FastAPI backend  →  AI/ML module
                        ↓
                   PostgreSQL
```

1. The user uploads a resume and the backend extracts its text.
2. The user submits a job description.
3. The backend sends both texts to the AI module's `analyze_resume()` function.
4. The result is saved and returned to the frontend.

## Project Structure

```
resume-analyzer/
├── backend/     # FastAPI app, database, AI integration
├── frontend/    # React app
└── README.md
```

## Getting Started

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then set your DATABASE_URL
createdb resume_analyzer
uvicorn main:app --reload
```

API docs: http://127.0.0.1:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

## API Endpoints

| Method | Endpoint | Description |

GET=>`/api/health` | Server status |
POST=>`/api/resume/upload` | Upload a PDF resume |
POST=>`/api/analyze` | Analyze a resume against a job description |
GET=>`/api/analysis/{id}` | Get one analysis |
GET=>`/api/history` | List recent analyses |

## Project Status

- [comp] Backend: upload, text extraction, database, analysis endpoints
- [comp ] AI/ML module integration (stub in use for now)
- [ ] Frontend
- [ ] DOCX support, login, deployment

