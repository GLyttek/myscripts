# Local RAG with Ollama

Local Retrieval-Augmented Generation using Ollama embeddings and PyTorch.

## Features

- **localrag.py** - Full RAG with query rewriting for better context retrieval
- **localrag_no_rewrite.py** - Simple RAG without query rewriting

## Requirements

```bash
conda install pytorch -c pytorch
pip install ollama openai
```

## Setup

1. Install Ollama and pull models:
```bash
ollama pull llama3
ollama pull mxbai-embed-large
```

2. Create a `vault.txt` file with your knowledge base content

3. Run:
```bash
python localrag.py
```

## How It Works

1. **Embedding**: Documents are embedded using `mxbai-embed-large`
2. **Query Rewriting**: User query is rewritten for better retrieval (optional)
3. **Retrieval**: Cosine similarity finds top-k relevant chunks
4. **Generation**: Ollama generates response with retrieved context

## Architecture

```
User Query → [Query Rewriter] → Embedding → Cosine Similarity → Top-K Context → LLM → Response
```

## Original Source

Experiments from 2024, based on easy-local-rag patterns.
