import os
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Import local helper modules
from parser import parse_resume
from analyzer import analyze_resume, optimize_single_bullet

app = FastAPI(
    title="AI Resume Analyzer API",
    description="Backend API for parsing resumes and analyzing them with Gemini AI",
    version="1.0.0"
)

# Enable CORS for React frontend (allows all origins for easy local setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BulletRequest(BaseModel):
    bullet_point: str

@app.get("/api/health")
def health_check():
    """
    Simple health check endpoint to verify backend status.
    """
    has_api_key = bool(os.getenv("GEMINI_API_KEY"))
    return {
        "status": "healthy",
        "api_key_configured": has_api_key,
        "mode": "Gemini API Active" if has_api_key else "Mock Fallback Mode"
    }

@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None)
):
    """
    Endpoint to upload a resume (PDF/DOCX) and compare it against an optional job description.
    """
    filename = file.filename
    # Read file bytes
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read upload file: {str(e)}"
        )

    # Parse resume text
    try:
        resume_text = parse_resume(filename, file_bytes)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing resume: {str(e)}"
        )

    # Analyze resume using Gemini/Mock
    try:
        jd_text = job_description if job_description else ""
        analysis_result = analyze_resume(resume_text, jd_text)
        return analysis_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/api/optimize-bullet")
def optimize_bullet(request: BulletRequest):
    """
    Endpoint to optimize a single bullet point using the Google XYZ formula.
    """
    try:
        result = optimize_single_bullet(request.bullet_point)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Optimization failed: {str(e)}"
        )

if __name__ == "__main__":
    # pyrefly: ignore [missing-import]
    import uvicorn
    # Start the server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
