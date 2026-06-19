%%writefile main.py
from typing import List
import pdfplumber
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from nlpengine import parse_profile
from recommender import JobRecommender
from matchscorer import rerank

app = FastAPI(title="PathFinder AI", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
recommender = JobRecommender()

class Job(BaseModel):
    id: int
    title: str
    company: str
    description: str
    skills: List[str] = []
    required_years: int = 0

@app.on_event("startup")
def seed_jobs():
    sample = [
        Job(id=1, title="Machine Learning Engineer", company="DeepCore",
            description="Build NLP models with Python, TensorFlow and deploy ML pipelines on AWS.",
            skills=["python", "tensorflow", "nlp", "aws", "machine learning"], required_years=3),
        Job(id=2, title="Frontend Engineer", company="Pixelate",
            description="Develop responsive UIs in React and TypeScript.",
            skills=["react", "javascript", "node.js"], required_years=2),
        Job(id=3, title="Data Analyst", company="InsightLabs",
            description="Analyze data with SQL, Python and Tableau.",
            skills=["sql", "python", "data analysis", "tableau"], required_years=1),
    ]
    recommender.add_jobs([j.model_dump() for j in sample])

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/match")
async def match_resume(file: UploadFile = File(...), top_k: int = 5):
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(400, "Upload a .pdf or .txt resume.")
    
    if file.filename.lower().endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    else:
        text = (await file.read()).decode("utf-8", errors="ignore")
        
    if not text.strip():
        raise HTTPException(422, "Could not read text from the file.")
        
    candidate = parse_profile(text)
    candidates = recommender.recommend(candidate["raw_text"], top_k=top_k)
    ranked = rerank(candidate, candidates)
    
    return {
        "profile": {"skills": candidate["skills"], "years_experience": candidate["years_experience"]},
        "matches": ranked,
    }
