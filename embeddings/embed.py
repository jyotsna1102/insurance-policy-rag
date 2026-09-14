from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed(self, text: str) -> list[float]:
        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )
        return vector.tolist()

    def embed_documents(self, texts: list[str]):
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

    def embed_query(self, query: str):
        vector = self.model.encode(
            query,
            normalize_embeddings=True,
        )
        return vector.tolist()