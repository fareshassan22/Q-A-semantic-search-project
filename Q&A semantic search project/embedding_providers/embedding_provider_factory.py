from embedding_providers.base_provider import BaseEmbeddingProvider, HuggingFaceEmbeddingProvider
from app.config import settings


class EmbeddingProviderFactory:
	@staticmethod
	def create_provider() -> BaseEmbeddingProvider:
		model_name = settings.embedding_model_name
		return HuggingFaceEmbeddingProvider(model_name)

