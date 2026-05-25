from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Connect to Qdrant
client = QdrantClient(
    host="qdrant",
    port=6333
)

COLLECTION_NAME = "rag_collection"


def create_collection():

    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print("Collection created")

    except Exception as e:
        print("Collection already exists")

def store_embedding(chunk_id, embedding, text):

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    "text": text
                }
            )
        ]
    )

    print(f"Stored chunk {chunk_id}")
def search_similar_chunks(query_embedding, limit=3):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit
    ).points

    return results    