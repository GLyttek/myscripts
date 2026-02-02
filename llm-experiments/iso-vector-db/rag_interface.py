"""
RAG (Retrieval-Augmented Generation) Interface

Combines vector database search with LLM generation for
context-aware question answering.

Usage:
    from rag_interface import RAGInterface

    rag = RAGInterface()
    rag.add_documents(["doc1", "doc2", ...])
    answer = rag.query("Your question?", model="llama3.2")
"""

import os
import numpy as np
from ollama_wrapper import OllamaWrapper
from vector_db import VectorDB

# Default system prompt for RAG
DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on
the provided context. If the context doesn't contain relevant information,
use your general knowledge but indicate this clearly."""


class RAGInterface:
    def __init__(self, dimension: int = 1024, embedding_model: str = "mxbai-embed-large"):
        """
        Initialize RAG interface.

        Args:
            dimension: Embedding dimension (1024 for mxbai-embed-large)
            embedding_model: Ollama model for embeddings
        """
        self.ollama = OllamaWrapper()
        self.vector_db = VectorDB(dimension=dimension)
        self.embedding_model = embedding_model
        self.system_prompt = os.getenv("RAG_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)

    def add_document(self, text: str):
        """Add a single document to the vector database."""
        embedding = self.ollama.embed(self.embedding_model, text)
        embedding_array = np.array(embedding['embedding'], dtype=np.float32)
        self.vector_db.add_text(text, embedding_array)

    def add_documents(self, texts: list):
        """Add multiple documents to the vector database."""
        for text in texts:
            self.add_document(text)
        print(f"Added {len(texts)} documents to vector database.")

    def query(self, question: str, model: str, k: int = 5, temperature: float = 0.7) -> str:
        """
        Query the RAG system.

        Args:
            question: User's question
            model: Ollama model for generation
            k: Number of context documents to retrieve
            temperature: LLM temperature

        Returns:
            Generated answer
        """
        # Get query embedding
        query_embedding = self.ollama.embed(self.embedding_model, question)
        query_array = np.array(query_embedding['embedding'], dtype=np.float32)

        # Search for similar documents
        similar_texts = self.vector_db.search(query_array, k)

        # Build prompt with context
        if similar_texts:
            context = "\n".join([f"- {text}" for text, _ in similar_texts])
            prompt = f"""Use the following context to answer the question.
If the context is not sufficient, use your general knowledge.

Context:
{context}

Question: {question}

Answer:"""
        else:
            prompt = f"Question: {question}\n\nAnswer:"

        # Generate response
        response = self.ollama.chat(
            model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": temperature}
        )

        answer = response['message']['content']

        # Optionally add Q&A to database for learning
        self.add_document(f"Q: {question}\nA: {answer}")

        return answer

    def list_models(self) -> list:
        """List available Ollama models."""
        models = self.ollama.list_models()
        return [m['name'] for m in models.get('models', [])]

    def save(self, filename: str = "rag_index"):
        """Save vector database to disk."""
        self.vector_db.save_index(filename)

    def load(self, filename: str = "rag_index"):
        """Load vector database from disk."""
        self.vector_db.load_index(filename)

    def get_stats(self) -> dict:
        """Get database statistics."""
        return {
            "documents": self.vector_db.get_size(),
            "trained": self.vector_db.is_trained,
            "dimension": self.vector_db.dimension
        }


def main():
    """Interactive RAG demo."""
    print("RAG Interface Demo")
    print("-" * 50)

    rag = RAGInterface()

    # List available models
    models = rag.list_models()
    print(f"Available models: {models[:5]}...")

    # Select model
    default_model = os.getenv("OLLAMA_MODEL", "llama3.2")
    model = input(f"Select model [{default_model}]: ").strip() or default_model

    # Load existing index or start fresh
    try:
        rag.load("rag_index")
        print(f"Loaded existing index with {rag.get_stats()['documents']} documents.")
    except FileNotFoundError:
        print("No existing index found. Starting fresh.")

        # Add some sample documents
        sample_docs = input("Enter path to documents file (or press Enter to skip): ").strip()
        if sample_docs:
            with open(sample_docs, 'r') as f:
                docs = [line.strip() for line in f if line.strip()]
            rag.add_documents(docs)

    # Query loop
    print("\nEnter your questions (type 'quit' to exit):")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() == 'quit':
            break

        answer = rag.query(question, model=model)
        print(f"\nAssistant: {answer}")

    # Save index
    rag.save("rag_index")
    print("Index saved. Goodbye!")


if __name__ == "__main__":
    main()
