from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class VectorStore:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.index = None

        self.chunks = []

    def build_index(
        self,
        chunks
    ):

        self.chunks = chunks

        embeddings = self.model.encode(
            chunks
        )

        embeddings = np.array(
            embeddings
        ).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(
            embeddings
        )

    def search(
        self,
        query,
        top_k=10
    ):

        query_embedding = self.model.encode(
            [query]
        )

        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.chunks):

                results.append(
                    self.chunks[idx]
                )

        return results