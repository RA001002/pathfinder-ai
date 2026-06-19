%%writefile recommender.py
from typing import List, Dict
import faiss
import numpy as np
from nlpengine import embed

class JobRecommender:
    def __init__(self, embedding_dim: int = 384):
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.jobs: List[Dict] = []

    def add_jobs(self, jobs: List[Dict]) -> None:
        descriptions = [f"{j['title']} {j['description']}" for j in jobs]
        vectors = embed(descriptions).astype("float32")
        self.index.add(vectors)
        self.jobs.extend(jobs)

    def recommend(self, profile_text: str, top_k: int = 5) -> List[Dict]:
        if self.index.ntotal == 0:
            return []
        query_vec = embed([profile_text]).astype("float32")
        top_k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_vec, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            job = dict(self.jobs[idx])
            job["match_score"] = round(float((score + 1) / 2 * 100), 1)
            results.append(job)
        return results
