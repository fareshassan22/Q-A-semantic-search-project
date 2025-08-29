# import os
# import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from fastapi import FastAPI, HTTPException
# from schemas import QueryRequest, QueryResponse, IndexRequest, IndexResponse
# from embedding_providers.hugging_face_provider import HuggingFaceEmbeddingProvider
# from data_base.operation import QdrantOperation
# from services.question_answer_service import QuestionAnswerService
# import time

# app = FastAPI()

# embedding_provider = HuggingFaceEmbeddingProvider("sentence-transformers/all-MiniLM-L6-v2")
# vector_repo = QdrantOperation("http://localhost:6333", "qa_collection", 384)
# qa_service = QuestionAnswerService(embedding_provider, vector_repo)

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {"status": "ok", "service": "Q&A Semantic Search System"}

# @app.get("/stats")
# async def get_stats():
#     """Get system statistics"""
#     try:
#         stats = qa_service.get_stats()
#         return stats
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

# @app.post("/index", response_model=IndexResponse)
# async def index_qa_pairs(request: IndexRequest):
#     """Index Q&A pairs into the system"""
#     try:
#         start_time = time.time()
#         indexed_count = qa_service.index_qa_pairs(request.pairs)
#         response_time = int((time.time() - start_time) * 1000)
        
#         return IndexResponse(
#             indexed_count=indexed_count,
#             success=True,
#             message=f"Successfully indexed {indexed_count} Q&A pairs in {response_time}ms"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

# @app.post("/query", response_model=QueryResponse)
# async def query_system(request: QueryRequest):
#     """Search for answers using semantic similarity"""
#     try:
#         start_time = time.time()
#         result = qa_service.search_answer(request.query)
#         response_time = int((time.time() - start_time) * 1000)
        
#         return QueryResponse(
#             query=request.query,
#             matched_question=result.get("question", ""),
#             answer=result.get("answer", ""),
#             similarity_score=result.get("similarity", 0.0),
#             response_time_ms=response_time
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# @app.delete("/delete/{question_id}")
# async def delete_qa_pair(question_id: str):
#     """Delete a specific Q&A pair by ID"""
#     try:
#         success = qa_service.delete_qa_pair(question_id)
#         if success:
#             return {"message": f"Successfully deleted Q&A pair with ID: {question_id}"}
#         else:
#             raise HTTPException(status_code=404, detail="Q&A pair not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

# @app.delete("/clear")
# async def clear_all_qa_pairs():
#     """Clear all Q&A pairs from the system"""
#     try:
#         deleted_count = qa_service.clear_all_qa_pairs()
#         return {"message": f"Successfully cleared {deleted_count} Q&A pairs"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Clear operation failed: {str(e)}")

# @app.get("/")
# def root():
#     return {"message": "Hello, world"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
