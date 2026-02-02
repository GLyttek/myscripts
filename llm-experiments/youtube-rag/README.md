# YouTube RAG

RAG system for querying YouTube video transcripts.

## Features

- Download and process YouTube transcripts
- Embed transcripts for semantic search
- Query video content with natural language

## Requirements

```bash
pip install ollama openai youtube-transcript-api
```

## Files

- **yt1.py** - Basic YouTube transcript RAG
- **yt-rag.py** - Enhanced version with better chunking

## Usage

```bash
python yt1.py --url "https://youtube.com/watch?v=VIDEO_ID"
```

## How It Works

1. **Transcript**: Downloads YouTube transcript via API
2. **Chunking**: Splits transcript into manageable segments
3. **Embedding**: Creates embeddings with Ollama
4. **Query**: Semantic search over video content

## Original Source

Experiments from 2024 for video content analysis.
