# Script Collection

This directory contains small utility scripts for working with AI models.
Each script is saved with a descriptive name and `.py` extension so they can be
run using Python.

## Scripts

### `claude_call.py`
Generates text using Anthropic's Claude API and outputs both a DOCX and HTML
file. It reads an outline, queries Claude for each section, and saves the
combined results.

### `groq_simple_chatbot.py`
A minimal command‑line chatbot using the Groq API. It keeps the conversation
context in memory and prints replies to the terminal.

### `read_mp3_summary.py`
Transcribes an MP3 using Faster Whisper, summarizes it with the Groq API, and
creates expert opinions from different perspectives.

### `testing_local_model.py`
Evaluates two local models via Ollama. It generates instructions in German and
saves the results as DOCX files.

