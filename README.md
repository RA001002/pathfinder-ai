# pathfinder-ai 
Powered Career & Job Matching Platform using Python, TensorFlow, NLP, React
<img width="1664" height="704" alt="1781855989" src="https://github.com/user-attachments/assets/7514788b-259f-418d-87fe-b41e4a732fe1" />

Developed an AI-powered career platform to semantically match unstructured resumes with open job descriptions.
Executed using FAISS for millisecond vector search across 2M+ profiles and spaCy for automated skill extraction.
The hybrid approach combines semantic embeddings + TensorFlow re-ranking to optimize job-candidate match accuracy.

An AI-powered career and job matching platform that parses unstructured resumes, extracts structured skills, and recommends the best-fit jobs using semantic vector search and neural re-ranking.
# Overview
PathFinder AI solves the problem of keyword-based resume screening by understanding the context of a candidate's experience. Instead of just looking for exact keyword matches, it uses Natural Language Processing (NLP) and Semantic Search to match the underlying meaning of a resume to job descriptions.
It utilizes a classic Two-Stage Retrieval Pipeline:
Candidate Generation: Uses FAISS for millisecond vector search across millions of profiles.
Re-ranking: Uses a TensorFlow neural network to blend semantic similarity, hard skill overlap, and experience metrics for the final ranking.
# Key Features
Unstructured Data Parsing: Automatically extracts text from .pdf and .txt resumes using pdfplumber.
NLP Entity Extraction: Uses spaCy to identify organizations, technologies, and hard skills from raw text.
Semantic Embeddings: Converts text into 384-dimensional vectors using Sentence-BERT (all-MiniLM-L6-v2).
High-Speed Vector Search: Powered by FAISS, capable of scaling to millions of job embeddings with sub-millisecond latency.
Neural Re-ranking: A custom TensorFlow model fuses semantic similarity, skill overlap, and experience fit to output a final match score (0-100).
Asynchronous API: Built with FastAPI for high-performance, non-blocking request handling.
# Tech Stack
Category                Technologies
Backend                 Python, FastAPI, Uvicorn
Machine Learning        TensorFlow, Sentence-BERT, spaCy
Vector Database         FAISS (Facebook AI Similarity Search)
Data Processing         Pydantic, pdfplumber, NumPy, scikit-learn
Frontend                HTML5, Vanilla JavaScript, CSS
Deployment              Google Colab, Ngrok (for public tunneling)


<img width="1120" height="486" alt="image" src="https://github.com/user-attachments/assets/2ef58406-3ac5-4a95-b2bd-3a5039576716" />

