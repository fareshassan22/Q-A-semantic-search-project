#class inheriting from base class 
#implement the logices of the abstract methods

from .base_provider import BaseEmbeddingProvider
from sentence_transformers import SentenceTransformer
from typing import List

class HuggingFaceEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        
        return self.model.encode(texts).tolist()
      