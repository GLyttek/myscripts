"""
Ollama API wrapper for embeddings and chat.
"""

import os
import ollama
from dotenv import load_dotenv

load_dotenv()


class OllamaWrapper:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.client = ollama.Client(host=self.base_url)

    def list_models(self) -> dict:
        """List available models."""
        return self.client.list()

    def chat(self, model: str, messages: list, stream: bool = False, **kwargs) -> dict:
        """Chat completion."""
        return self.client.chat(model=model, messages=messages, stream=stream, **kwargs)

    def generate(self, model: str, prompt: str, stream: bool = False, **kwargs) -> dict:
        """Text generation."""
        return self.client.generate(model=model, prompt=prompt, stream=stream, **kwargs)

    def embed(self, model: str, text: str) -> dict:
        """Generate embeddings for text."""
        return self.client.embeddings(model=model, prompt=text)
