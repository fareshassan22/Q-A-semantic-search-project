import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import uuid


file_path = 'C:/Users/Arabtech/Downloads/Q&A semantic search project/QnA-dataa - Sheet1.csv'
df=pd.read_csv(file_path)

qa_pairs=[]

for i in range(0,df.shape[1],2):
    if i+1 < df.shape[1]:
        q_col,a_col=df.columns[i+1], df.columns[i]
        for _,row in df.iterrows():
            question, answer = row[q_col], row[a_col]
            if pd.notna(question) and pd.notna(answer):
                qa_pairs.append((question, answer))

print(f"Extracted {len(qa_pairs)} Q&A pairs")


QDRANRT_URL = "http://localhost:6333"
collection_name = "qa_collection"
model_name = "all-MiniLM-L6-v2"
client = QdrantClient(url=QDRANRT_URL)

model = SentenceTransformer(model_name)
vector_Dim = model.get_sentence_embedding_dimension()
  
  