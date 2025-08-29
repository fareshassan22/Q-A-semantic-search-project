from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct, PayloadSchemaType, TextIndexParams, TokenizerType
from typing import List, Dict, Any, Optional
from uuid import uuid4


class QdrantOperation:
    def __init__(self, url: str, collection_name: str, vector_size: int, distance: Distance = Distance.COSINE):
        self.url = url
        self.collection_name = collection_name
        self.vector_size = int(vector_size)
        self.distance = distance

        self.client = QdrantClient(url=self.url)
        self._manage_collection()
        
    def _manage_collection(self):
        try:
            collections = self.client.get_collections().collections
            if self.collection_name not in [c.name for c in collections]:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=self.vector_size, distance=self.distance)
                )
            # Ensure payload/text indexes exist
            self._ensure_indexes()
        except Exception as e:
            print(f"Error ensuring collection: {e}")    
            
            raise

    def _ensure_indexes(self) -> None:
        """Create common payload indexes for Q&A data. Safe to call multiple times."""
        try:
            # Text index for question
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="question",
                field_schema=PayloadSchemaType.TEXT,
                schema=TextIndexParams(
                    tokenizer=TokenizerType.WORD,
                    min_token_len=2,
                    max_token_len=20,
                    lowercase=True,
                ),
            )
        except Exception:
            # Ignore if index already exists or server does not support this exact API
            pass

        # Keyword-like fields
        for field_name in [
            "source",
            "url",
            "doc_id",
            "provider",
            "model_version",
            "tags",
        ]:
            try:
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name=field_name,
                    field_schema=PayloadSchemaType.KEYWORD,
                )
            except Exception:
                pass

    def insert(self,vectors:List[List[float]], payloads:List[Dict[str,Any]])->int:
        try:
            if len(vectors) != len(payloads):
                raise ValueError("Vectors and payloads length mismatch")
            for v in vectors:
                if len(v) != self.vector_size:
                    raise ValueError("One or more vectors have incorrect dimension")
            points = [
                PointStruct(id=str(uuid4()), vector=vectors[i], payload=payloads[i])
                for i in range(len(vectors))
            ]
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return len(points)
        except Exception as e:
            print(f"Error inserting points: {e}")
            raise
    
    def search(self, vector: List[float], top_k: int = 1, query_filter: Optional[Any] = None) -> List[Dict[str, Any]]:
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=top_k,
                query_filter=query_filter,
                with_payload=True,
                with_vectors=False,
            )
            return [{"id": r.id, "score": r.score, "payload": r.payload} for r in results]
        except Exception as e:
            print(f"Error searching vectors: {e}")
            return []
        
     
    def delete_collection(self): 
      try:
            self.client.delete_collection(collection_name=self.collection_name)
            print(f"Collection '{self.collection_name}' deleted.")
      except Exception as e:
            print(f"[Error] Deleting collection failed: {e}")