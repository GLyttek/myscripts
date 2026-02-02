"""
FAISS-based Vector Database with auto-optimization.

Features:
- IVF (Inverted File) index for efficient similarity search
- Automatic training when enough vectors are collected
- Bayesian optimization for index parameters
- Persistence (save/load)
"""

import faiss
import numpy as np
import pickle

# Optional: scikit-optimize for index tuning
try:
    from skopt import gp_minimize
    from skopt.space import Integer
    from skopt.utils import use_named_args
    SKOPT_AVAILABLE = True
except ImportError:
    SKOPT_AVAILABLE = False


class VectorDB:
    def __init__(self, dimension: int = 1024):
        """
        Initialize vector database.

        Args:
            dimension: Embedding dimension (must match your embedding model)
        """
        self.dimension = dimension
        self.quantizer = faiss.IndexFlatL2(self.dimension)
        self.index = faiss.IndexIVFFlat(self.quantizer, self.dimension, 100)
        self.texts = []
        self.vectors = []
        self.is_trained = False

    def add_text(self, text: str, embedding: np.ndarray):
        """Add a text with its embedding to the database."""
        if text not in self.texts:
            self.vectors.append(embedding)
            self.texts.append(text)

            # Train index when we have enough vectors
            if not self.is_trained and len(self.vectors) >= 100:
                self.train()
            elif self.is_trained:
                self.index.add(np.array([embedding]))

            # Optimize periodically
            if SKOPT_AVAILABLE and len(self.vectors) % 10000 == 0:
                self.optimize_index()

    def search(self, query_embedding: np.ndarray, k: int = 5) -> list:
        """
        Search for similar texts.

        Returns:
            List of (text, distance) tuples
        """
        if not self.is_trained:
            print("Index is not trained yet. Need at least 100 vectors.")
            return []

        distances, indices = self.index.search(query_embedding.reshape(1, -1), k)
        return [
            (self.texts[i], distances[0][j])
            for j, i in enumerate(indices[0])
            if i < len(self.texts)
        ]

    def train(self):
        """Train the IVF index."""
        if len(self.vectors) < 100:
            print(f"Not enough vectors to train. Current: {len(self.vectors)}, Required: 100")
            return

        self.index.train(np.array(self.vectors))
        self.is_trained = True
        self.index.add(np.array(self.vectors))
        print(f"Index trained with {len(self.vectors)} vectors.")

    def optimize_index(self):
        """Use Bayesian optimization to find optimal index parameters."""
        if not SKOPT_AVAILABLE:
            print("scikit-optimize not installed. Skipping optimization.")
            return

        if len(self.vectors) < 10000:
            return

        dimensions = [
            Integer(10, min(1000, len(self.vectors) // 100), name='nlist'),
            Integer(1, 100, name='nprobe')
        ]

        @use_named_args(dimensions=dimensions)
        def objective(nlist, nprobe):
            index = faiss.IndexIVFFlat(self.quantizer, self.dimension, int(nlist))
            index.train(np.array(self.vectors))
            index.add(np.array(self.vectors))
            index.nprobe = int(nprobe)
            random_query = np.random.random((1, self.dimension)).astype('float32')
            distances, _ = index.search(random_query, 10)
            return distances.mean()

        result = gp_minimize(objective, dimensions, n_calls=50, random_state=42)
        optimal_nlist, optimal_nprobe = result.x

        self.index = faiss.IndexIVFFlat(self.quantizer, self.dimension, int(optimal_nlist))
        self.train()
        self.index.nprobe = int(optimal_nprobe)
        print(f"Optimized: nlist={optimal_nlist}, nprobe={optimal_nprobe}")

    def save_index(self, filename: str = "vector_db"):
        """Save index to disk."""
        faiss.write_index(self.index, f"{filename}.faiss")
        with open(f"{filename}.pkl", "wb") as f:
            pickle.dump((self.texts, self.vectors, self.is_trained), f)
        print(f"Saved to {filename}.faiss and {filename}.pkl")

    def load_index(self, filename: str = "vector_db"):
        """Load index from disk."""
        self.index = faiss.read_index(f"{filename}.faiss")
        with open(f"{filename}.pkl", "rb") as f:
            self.texts, self.vectors, self.is_trained = pickle.load(f)
        print(f"Loaded {len(self.texts)} vectors from {filename}")

    def get_size(self) -> int:
        """Return number of stored texts."""
        return len(self.texts)
