from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    matched_question: str
    answer: str
    similarity_score: float
    response_time_ms: int

class QAPair(BaseModel):
    question: str
    answer: str

class IndexRequest(BaseModel):
    pairs: List[QAPair]

class IndexResponse(BaseModel):
    indexed_count: int
    success: bool
    message: Optional[str] = None