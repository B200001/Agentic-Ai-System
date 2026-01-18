from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid


class QdrantMemory:
    def __init__(self, collection_name="agent_memory"):
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")  # free + fast

        self._init_collection()

    def _init_collection(self):
        collections = [c.name for c in self.client.get_collections().collections]

        if self.collection_name not in collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

    def add_text(self, text: str, metadata: dict = None):
        vector = self.embedder.encode(str(text)).tolist()
        point_id = str(uuid.uuid4())

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={"text": text, "metadata": metadata or {}}
                )
            ]
        )
    def search(self, query, limit: int = 5, min_score: float = 0.55):
        if isinstance(query, set):
            query = " ".join(list(query))
        query = str(query)
    
        q_vector = self.embedder.encode(query).tolist()
    
        hits = self.client.query_points(
            collection_name=self.collection_name,
            query=q_vector,
            limit=limit
        ).points
    
        results = [
            {
                "text": hit.payload.get("text"),
                "metadata": hit.payload.get("metadata"),
                "score": hit.score
            }
            for hit in hits
        ]
    
        # ✅ keep only relevant memory
        filtered = [r for r in results if r["score"] >= min_score]
        return filtered


    def count(self) -> int:
        info = self.client.get_collection(self.collection_name)
        return info.points_count

    def peek(self, limit: int = 5):
        points = self.client.scroll(
            collection_name=self.collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )[0]

        return [
            {
                "text": p.payload.get("text"),
                "metadata": p.payload.get("metadata"),
            }
            for p in points
        ]
