from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json

from app.config import settings
from app.agent import agent

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


# ---------- 1. Parse an uploaded resume ----------
@app.post("/api/resume/parse")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    if file.size and file.size > settings.MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(400, f"File too large. Max {settings.MAX_UPLOAD_MB}MB.")
    file_bytes = await file.read()
    try:
        return agent.parse_resume(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(400, str(e))


# ---------- 2. Analyze a job description ----------
class JDRequest(BaseModel):
    job_description: str

@app.post("/api/jd/analyze")
def analyze_jd_endpoint(req: JDRequest):
    try:
        return agent.analyze_job(req.job_description)
    except ValueError as e:
        raise HTTPException(400, str(e))


# ---------- 3. ATS score (resume vs JD) ----------
class ATSRequest(BaseModel):
    resume_json: dict
    jd_analysis: dict

@app.post("/api/resume/ats-score")
def ats_score_endpoint(req: ATSRequest):
    return agent.ats_score(req.resume_json, req.jd_analysis)


# ---------- 4. Skill gap analysis + learning resources ----------
class GapRequest(BaseModel):
    resume_json: dict
    jd_analysis: dict

@app.post("/api/resume/gap-analysis")
def gap_analysis_endpoint(req: GapRequest):
    report = agent.gap_analysis(req.resume_json, req.jd_analysis)
    return {"report": report}


# ---------- 5. Tailor an existing resume to a JD ----------
class TailorRequest(BaseModel):
    resume_json: dict
    jd_analysis: dict

@app.post("/api/resume/tailor")
def tailor_resume_endpoint(req: TailorRequest):
    return agent.tailor_resume(req.resume_json, req.jd_analysis)


# ---------- 6. Build a resume from scratch ----------
class BuildRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    linkedin: Optional[str] = ""
    github: Optional[str] = ""
    education: str          # free text, e.g. "B.Tech CSE, XYZ College, 2026, 8.2 CGPA"
    skills: str              # free text or comma-separated
    projects: str            # free text description of projects/internships
    target_role: Optional[str] = ""

@app.post("/api/resume/build")
def build_resume_endpoint(req: BuildRequest):
    return agent.build_resume(req.model_dump())
