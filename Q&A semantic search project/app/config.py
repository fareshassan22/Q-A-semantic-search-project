from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class AppSettings(BaseSettings):
	qdrant_host: str = Field(default="localhost", alias="QDRANT_HOST")
	qdrant_port: int = Field(default=6333, alias="QDRANT_PORT")
	# Accept both COLLECTION_NAME and legacy QDRANT_COLLECTION
	collection_name: str = Field(default="qa_pairs", alias="COLLECTION_NAME")
	embedding_model_name: str = Field(default="thenlper/gte-small", alias="EMBEDDING_MODEL")
	# Accept both SIMILARITY_METRIC and legacy SIMILARITY
	similarity_metric: str = Field(default="cosine", alias="SIMILARITY_METRIC")
	batch_size: int = Field(default=64, alias="BATCH_SIZE")
	cors_allow_all: bool = Field(default=True, alias="CORS_ALLOW_ALL")
	qdrant_url: Optional[str] = Field(default=None, alias="QDRANT_URL")

	model_config = SettingsConfigDict(
		env_file="dot.env",
		env_file_encoding="utf-8",
		case_sensitive=False,
		# Ignore unexpected env keys (e.g., QDRANT_COLLECTION, SIMILARITY)
		extra="ignore",
	)


settings = AppSettings()
