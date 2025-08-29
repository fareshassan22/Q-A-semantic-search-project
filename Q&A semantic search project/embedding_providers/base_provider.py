#abstract class
from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Return embedding vectors for the given list of texts."""
        raise NotImplementedError


class HuggingFaceEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()