%%writefile matchscorer.py
import numpy as np
import tensorflow as tf

def build_model() -> tf.keras.Model:
    inputs = tf.keras.Input(shape=(3,))
    x = tf.keras.layers.Dense(8, activation="relu")(inputs)
    x = tf.keras.layers.Dense(4, activation="relu")(x)
    out = tf.keras.layers.Dense(1, activation="sigmoid")(x)
    model = tf.keras.Model(inputs, out)
    model.compile(optimizer="adam", loss="binary_crossentropy")
    return model

MODEL = build_model()

def skill_overlap(candidate_skills, job_skills) -> float:
    if not job_skills: return 0.0
    cand, job = set(candidate_skills), set(job_skills)
    return len(cand & job) / len(job)

def experience_fit(cand_years: int, required_years: int) -> float:
    if required_years == 0: return 1.0
    return min(cand_years / required_years, 1.0)

def rerank(candidate, jobs):
    for job in jobs:
        sem = job["match_score"] / 100
        overlap = skill_overlap(candidate["skills"], job.get("skills", []))
        exp = experience_fit(candidate["years_experience"], job.get("required_years", 0))
        
        features = np.array([[sem, overlap, exp]], dtype="float32")
        model_score = float(MODEL(features).numpy()[0][0])
        
        job["match_score"] = round((0.6 * sem + 0.25 * overlap + 0.15 * exp) * 100, 1)
        job["model_signal"] = round(model_score, 3)
    return sorted(jobs, key=lambda j: j["match_score"], reverse=True)
