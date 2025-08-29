from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
import numpy as np


class VectorRepository(ABC):
	@abstractmethod
	def ensure_collection(self, name: str, vector_size: int, distance: str = "cosine") -> None:
		...

	@abstractmethod
	def upsert(self, collection: str, vectors: np.ndarray, payloads: List[Dict[str, Any]]) -> int:
		...

	@abstractmethod
	def search(self, collection: str, vector: np.ndarray, limit: int = 1) -> List[Tuple[float, Dict[str, Any]]]:
		...

	@abstractmethod
	def count(self, collection: str) -> int:
		...


class QdrantVectorRepository(VectorRepository):
	def __init__(self, host: str, port: int) -> None:
		self.client = QdrantClient(host=host, port=port)

	def ensure_collection(self, name: str, vector_size: int, distance: str = "cosine") -> None:
		metric = {
			"cosine": rest.Distance.COSINE,
			"dot": rest.Distance.DOT,
			"euclid": rest.Distance.EUCLID,
		}.get(distance, rest.Distance.COSINE)
		try:
			self.client.get_collection(name)
		except Exception:
			self.client.recreate_collection(
				collection_name=name,
				vectors_config=rest.VectorParams(size=vector_size, distance=metric),
			)

	def upsert(self, collection: str, vectors: np.ndarray, payloads: List[Dict[str, Any]]) -> int:
		points = []
		for idx, (vec, payload) in enumerate(zip(vectors, payloads)):
			points.append(
				rest.PointStruct(id=None, vector=vec.tolist(), payload=payload)
			)
		operation_info = self.client.upsert(collection_name=collection, points=points)
		return len(points)

	def search(self, collection: str, vector: np.ndarray, limit: int = 1) -> List[Tuple[float, Dict[str, Any]]]:
		results = self.client.search(
			collection_name=collection,
			query_vector=vector.tolist(),
			limit=limit,
			with_payload=True,
		)
		return [
			(float(r.score), dict(r.payload or {}))
			for r in results
		]

	def count(self, collection: str) -> int:
		res = self.client.count(collection_name=collection, exact=True)
		return int(res.count or 0)

