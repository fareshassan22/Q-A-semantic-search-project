from abc import ABC, abstractmethod
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService(ABC):
	@abstractmethod
	def embed(self, texts: List[str]) -> np.ndarray:
		...

	@abstractmethod
	def dimension(self) -> int:
		...


class SentenceTransformerEmbeddingService(EmbeddingService):
	def __init__(self, model_name: str) -> None:
		self._model = SentenceTransformer(model_name)
		# Warm-up to ensure consistent dims
		self._dim = int(self._model.get_sentence_embedding_dimension())

	def embed(self, texts: List[str]) -> np.ndarray:
		vectors = self._model.encode(texts, batch_size=64, convert_to_numpy=True, normalize_embeddings=False)
		return np.asarray(vectors, dtype=np.float32)

	def dimension(self) -> int:
		return self._dim


class EmbeddingFactory:
	@staticmethod
	def create(model_name: str) -> EmbeddingService:
		# Future: add more model types here
		return SentenceTransformerEmbeddingService(model_name)

