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
    file: Optional[UploadFile] = File(None),
    resume_text_input: Optional[str] = Form(None, alias="resume_text"),
    job_description: Optional[str] = Form(None),
    job_description_file: Optional[UploadFile] = File(None)
):
    """
    Endpoint to upload a resume (PDF/DOCX) or raw text and compare it against an optional job description.
    """
    resume_text = ""
    
    if file and file.filename:
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
    elif resume_text_input and resume_text_input.strip():
        resume_text = resume_text_input.strip()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must provide either a resume file or raw resume text."
        )

    # Parse job description if uploaded as a file
    jd_text = ""
    if job_description_file and job_description_file.filename:
        try:
            jd_bytes = await job_description_file.read()
            ext = os.path.splitext(job_description_file.filename.lower())[1]
            if ext == ".txt":
                try:
                    jd_text = jd_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    jd_text = jd_bytes.decode('latin-1')
            else:
                jd_text = parse_resume(job_description_file.filename, jd_bytes)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to parse job description file: {str(e)}"
            )
    elif job_description:
        jd_text = job_description

    # Analyze resume using Gemini/Mock
    try:
        analysis_result = analyze_resume(resume_text, jd_text)
        if "error" in analysis_result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=analysis_result["error"]
            )
        return analysis_result
    except HTTPException:
        raise
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
class ScrapeRequest(BaseModel):
    url: str

@app.post("/api/scrape-jd")
def scrape_jd_endpoint(request: ScrapeRequest):
    """
    Endpoint to scrape and extract a job description from a URL using Gemini/mock.
    """
    url = request.url.strip()
    if not url or not url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL. Please enter a valid link starting with http:// or https://"
        )
        
    try:
        import requests
        from html.parser import HTMLParser
        
        class HTMLTextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.ignore = False

            def handle_starttag(self, tag, attrs):
                if tag in ["script", "style", "head", "title", "meta", "link", "svg", "path"]:
                    self.ignore = True

            def handle_endtag(self, tag):
                if tag in ["script", "style", "head", "title", "meta", "link", "svg", "path"]:
                    self.ignore = False

            def handle_data(self, data):
                if not self.ignore and data.strip():
                    self.text.append(data.strip())

            def get_text(self):
                return "\n".join(self.text)
                
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch page. HTTP Status: {response.status_code}"
            )
            
        extractor = HTMLTextExtractor()
        extractor.feed(response.text)
        raw_text = extractor.get_text()
        
        # Prevent token size issues
        max_chars = 12000
        if len(raw_text) > max_chars:
            raw_text = raw_text[:max_chars] + "\n...[truncated]..."
            
        # Parse job details using Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            system_prompt = (
                "You are an expert recruitment assistant. Extract the job description from the provided noisy webpage text.\n"
                "Identify and extract the Job Title, Company Name, and the full content of the Job Description (responsibilities, qualifications, and requirements).\n"
                "Output the results cleanly structured in standard Markdown. Do not include headers/footers, sidebars, navigation links, or other page noise.\n"
                "If the text does not contain a job posting, respond with 'Error: Could not extract job details from this link.'"
            )
            
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=system_prompt
            )
            
            ai_response = model.generate_content(f"WEBPAGE TEXT:\n{raw_text}")
            extracted = ai_response.text.strip()
            
            if extracted.startswith("Error:"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=extracted
                )
                
            return {"job_description": extracted}
        else:
            # Fallback simple text preview
            lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
            preview = "\n".join(lines[:25])
            return {"job_description": f"=== Scraped Text Preview ===\n{preview}"}
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scraping failed: {str(e)}"
        )


if __name__ == "__main__":
    # pyrefly: ignore [missing-import]
    import uvicorn
    # Start the server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
