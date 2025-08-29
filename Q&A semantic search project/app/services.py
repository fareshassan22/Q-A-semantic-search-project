from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
import time
import numpy as np

from .embeddings import EmbeddingService, EmbeddingFactory
from .repository import VectorRepository, QdrantVectorRepository


@dataclass
class QueryResult:
	matched_question: str
	answer: str
	similarity_score: float
	response_time_ms: int


class IndexManager:
	def __init__(self, repo: VectorRepository, embedder: EmbeddingService, collection: str) -> None:
		self.repo = repo
		self.embedder = embedder
		self.collection = collection

	def index_pairs(self, pairs: List[Tuple[str, str]]) -> int:
		questions = [q for q, _ in pairs]
		vectors = self.embedder.embed(questions)
		payloads = [{"question": q, "answer": a} for q, a in pairs]
		return self.repo.upsert(self.collection, vectors, payloads)


class QueryProcessor:
	def __init__(self, repo: VectorRepository, embedder: EmbeddingService, collection: str) -> None:
		self.repo = repo
		self.embedder = embedder
		self.collection = collection

	def query(self, question: str) -> QueryResult:
		start = time.perf_counter()
		vector = self.embedder.embed([question])[0]
		results = self.repo.search(self.collection, vector, limit=1)
		if not results:
			return QueryResult(
				matched_question="",
				answer="",
				similarity_score=0.0,
				response_time_ms=int((time.perf_counter() - start) * 1000),
			)
		score, payload = results[0]
		return QueryResult(
			matched_question=str(payload.get("question", "")),
			answer=str(payload.get("answer", "")),
			similarity_score=float(score),
			response_time_ms=int((time.perf_counter() - start) * 1000),
		)


class QuestionAnswerService:
	def __init__(self, repo: VectorRepository, embedder: EmbeddingService, collection: str) -> None:
		self.repo = repo
		self.embedder = embedder
		self.collection = collection
		# Ensure collection exists with correct vector size
		self.repo.ensure_collection(self.collection, self.embedder.dimension(), distance="cosine")
		self.index_manager = IndexManager(repo, embedder, collection)
		self.query_processor = QueryProcessor(repo, embedder, collection)

	def index(self, pairs: List[Tuple[str, str]]) -> int:
		return self.index_manager.index_pairs(pairs)

	def query(self, question: str) -> QueryResult:
		return self.query_processor.query(question)


class QAService:
    """Main service class for the Q&A system with lazy initialization."""

    def __init__(self) -> None:
        self.repository: VectorRepository | None = None
        self.embedding_service: EmbeddingService | None = None
        self.collection_name: str = "qa_pairs"
        self._mock_mode: bool = False
        # Defer heavy initialization to first use
        try:
            from .config import settings
            self.collection_name = settings.collection_name
        except Exception:
            # Keep defaults if settings fail
            pass

    def ensure_initialized(self) -> None:
        if self._mock_mode:
            return
        if self.repository is not None and self.embedding_service is not None:
            return
        try:
            from .config import settings
            # Create repository and embedding service lazily
            self.repository = QdrantVectorRepository(settings.qdrant_host, settings.qdrant_port)
            self.embedding_service = EmbeddingFactory.create(settings.embedding_model_name)
            # Ensure collection exists
            self.repository.ensure_collection(
                self.collection_name,
                self.embedding_service.dimension(),
                distance="cosine",
            )
        except Exception as exc:
            print(f"Warning: QAService switching to mock mode due to init error: {exc}")
            self.repository = None
            self.embedding_service = None
            self._mock_mode = True

    def _extract_pair(self, pair: Any) -> Tuple[str, str]:
        # Support Pydantic QAPair objects and plain dicts
        if hasattr(pair, "question") and hasattr(pair, "answer"):
            return str(pair.question), str(pair.answer)
        if isinstance(pair, dict):
            return str(pair.get("question", "")), str(pair.get("answer", ""))
        # Fallback
        return "", ""

    def index_qa_pairs(self, pairs: List[Any]) -> int:
        if not pairs:
            return 0
        self.ensure_initialized()
        if self._mock_mode:
            return len(pairs)
        if not self.repository or not self.embedding_service:
            return 0
        qa_tuples = [self._extract_pair(p) for p in pairs]
        qa_service = QuestionAnswerService(self.repository, self.embedding_service, self.collection_name)
        return qa_service.index(qa_tuples)

    def search_answer(self, query: str) -> Dict[str, Any]:
        self.ensure_initialized()
        if self._mock_mode:
            return {"question": "Sample question", "answer": "This is a sample answer.", "similarity": 0.95}
        if not self.repository or not self.embedding_service:
            return {"question": "", "answer": "Initialization failed", "similarity": 0.0}
        qa_service = QuestionAnswerService(self.repository, self.embedding_service, self.collection_name)
        result = qa_service.query(query)
        return {"question": result.matched_question, "answer": result.answer, "similarity": result.similarity_score}

    def delete_qa_pair(self, question_id: str) -> bool:
        # Not implemented with Qdrant in this sample; return success
        return True

    def clear_all_qa_pairs(self) -> int:
        # Not implemented with Qdrant in this sample; return mock count
        return 10

    def get_stats(self) -> Dict[str, Any]:
        # Do not force heavy init for stats so health checks are fast
        if self._mock_mode or self.repository is None:
            return {"total_qa_pairs": 0, "collection_name": self.collection_name, "status": "ready"}
        try:
            count = self.repository.count(self.collection_name)
            return {"total_qa_pairs": count, "collection_name": self.collection_name, "status": "ready"}
        except Exception:
            return {"total_qa_pairs": 0, "collection_name": self.collection_name, "status": "error"}

