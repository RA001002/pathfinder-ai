%%writefile nlpengine.py
import re
from typing import List, Dict
import spacy
from sentence_transformers import SentenceTransformer

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
NLP = spacy.load("en_core_web_sm")

SKILL_LEXICON = {
    "python", "java", "javascript", "react", "tensorflow", "pytorch",
    "nlp", "sql", "aws", "docker", "kubernetes", "machine learning",
    "data analysis", "fastapi", "node.js", "go", "rust", "tableau",
    "excel", "communication", "leadership", "project management",
}

EXPERIENCE_RE = re.compile(r"(\d+)\+?\s(?:years?|yrs?)", re.IGNORECASE)

def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    found = {skill for skill in SKILL_LEXICON if skill in text_lower}
    doc = NLP(text)
    for ent in doc.ents:
        if ent.label_ in {"ORG", "PRODUCT"} and len(ent.text) < 25:
            found.add(ent.text.lower())
    return sorted(found)

def extract_years_experience(text: str) -> int:
    matches = EXPERIENCE_RE.findall(text)
    return max((int(m) for m in matches), default=0)

def parse_profile(text: str) -> Dict:
    return {
        "skills": extract_skills(text),
        "years_experience": extract_years_experience(text),
        "raw_text": text,
    }

def embed(texts: List[str]):
    return EMBED_MODEL.encode(
        texts, normalize_embeddings=True, show_progress_bar=False
    )
