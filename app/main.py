from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
import json

from app.config import settings
from app.agent import agent
from app.tools.pdf_generator import generate_resume_pdf

settings.validate()

app = FastAPI(title="AI Resume Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/resume/parse")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    if file.size and file.size > settings.MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(400, f"File too large. Max {settings.MAX_UPLOAD_MB}MB.")
    file_bytes = await file.read()
    try:
        return agent.parse_resume(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(400, str(e))


class JDRequest(BaseModel):
    job_description: str

@app.post("/api/jd/analyze")
def analyze_jd_endpoint(req: JDRequest):
    try:
        return agent.analyze_job(req.job_description)
    except ValueError as e:
        raise HTTPException(400, str(e))


class ATSRequest(BaseModel):
    resume_json: dict
    jd_analysis: dict

@app.post("/api/resume/ats-score")
def ats_score_endpoint(req: ATSRequest):
    return agent.ats_score(req.resume_json, req.jd_analysis)


class GapRequest(BaseModel):
    resume_json: dict
    jd_analysis: dict

@app.post("/api/resume/gap-analysis")
def gap_analysis_endpoint(req: GapRequest):
    report = agent.gap_analysis(req.resume_json, req.jd_analysis)
    return {"report": report}


class TailorRequest(BaseModel):
    resume_json: dict
    jd_analysis: dict

@app.post("/api/resume/tailor")
def tailor_resume_endpoint(req: TailorRequest):
    return agent.tailor_resume(req.resume_json, req.jd_analysis)


class BuildRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    linkedin: Optional[str] = ""
    github: Optional[str] = ""
    education: str
    skills: str
    projects: str
    target_role: Optional[str] = ""

@app.post("/api/resume/build")
def build_resume_endpoint(req: BuildRequest):
    return agent.build_resume(req.model_dump())


class PdfRequest(BaseModel):
    resume_json: dict

@app.post("/api/resume/download-pdf")
def download_pdf_endpoint(req: PdfRequest):
    try:
        pdf_bytes = generate_resume_pdf(req.resume_json)
    except Exception as e:
        raise HTTPException(500, f"Could not generate PDF: {e}")

    filename = f"{req.resume_json.get('name', 'resume').replace(' ', '_')}_Resume.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
