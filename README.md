# My Scripts

This repository contains small Python utilities for interacting with AI models.
All scripts are located in the `scripts/` directory.

## Available Scripts

- **claude_call.py** – Query Anthropic's Claude model and save results to a DOCX
  and HTML file.
- **groq_simple_chatbot.py** – Simple terminal chatbot using the Groq API.
- **read_mp3_summary.py** – Transcribe an MP3 file, summarize it, and generate
  expert opinions using the Groq API.
- **testing_local_model.py** – Evaluate local models with Ollama and save the
  outputs.

See [scripts/README.md](scripts/README.md) for more details on each script.

## SOAR Framework

The `soar_framework` package provides a minimal incident response
automation framework. It demonstrates dynamic playbook execution with
stub integrations for SIEM, EDR and cloud security APIs. An Ollama-based
LLM is used to generate forensic documentation such as chain of custody
records and incident reports.

Run `python -m soar_framework.main` to execute the sample playbook.

