# My Scripts

This repository contains small Python utilities for interacting with AI models.
All scripts are located in the `scripts/` directory.

## Setup

Create the conda environment and install the required Python packages:

```bash
conda env create -f environment.yml
conda activate myscripts
```

## Available Scripts

- **claude_call.py** – Query Anthropic's Claude model and save results to a DOCX
  and HTML file.
- **groq_simple_chatbot.py** – Simple terminal chatbot using the Groq API.
- **read_mp3_summary.py** – Transcribe an MP3 file, summarize it, and generate
  expert opinions using the Groq API.
- **testing_local_model.py** – Evaluate local models with Ollama and save the
  outputs.

See [scripts/README.md](scripts/README.md) for more details on each script.

## LLM Experiments

The `llm-experiments/` directory contains more advanced AI experiments:

- **mitre-attack/** – Extract MITRE ATT&CK TTPs from cybersecurity scenarios
- **iso-vector-db/** – RAG system with FAISS vector database
- **security-awareness/** – Generate security awareness training content

See [llm-experiments/README.md](llm-experiments/README.md) for details.

## Monitoring App

The `monitoring-app/` directory contains a system monitoring demo with FastAPI
backend and React frontend. See its README for setup instructions.

## Related

- [Lyttek AI Journey](https://github.com/GLyttek/lyttek-ai-journey) – Documentation of our AI automation journey
