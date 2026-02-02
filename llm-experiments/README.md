# LLM Experiments

A collection of practical LLM experiments focusing on security, RAG, and content generation.

## Projects

### 1. MITRE ATT&CK TTP Analyzer (`mitre-attack/`)

Extracts Tactics, Techniques, and Procedures from cybersecurity scenarios using local LLMs.

```bash
cd mitre-attack
export OLLAMA_MODEL=llama3.2
python mitre_ttp_analyzer.py
```

**Features:**
- Natural language scenario input
- Automatic TTP extraction via LLM
- MITRE ATT&CK database search
- Example attack chain generation

**Requirements:**
- Ollama with any capable model
- MITRE ATT&CK dataset (`enterprise-attack.json`)
- `pip install ollama mitreattack-stix20`

---

### 2. RAG Vector Database (`iso-vector-db/`)

Retrieval-Augmented Generation system with FAISS vector database.

```bash
cd iso-vector-db
cp .env.example .env
pip install -r requirements.txt
python rag_interface.py
```

**Features:**
- FAISS-based vector storage
- Automatic index optimization (with scikit-optimize)
- Context-aware question answering
- Learning from Q&A history

**Use Cases:**
- Document Q&A systems
- Knowledge base search
- ISO/compliance document queries

---

### 3. Security Awareness Generator (`security-awareness/`)

Generates cybersecurity awareness training content for presentations.

```bash
cd security-awareness
export OLLAMA_MODEL=llama3.2
python awareness_generator.py
```

**Features:**
- Industry-specific content generation
- Slide outlines with speaker notes
- Optional Flux image generation
- Export to text format

---

## Setup

All projects use Ollama for local LLM inference.

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.2

# Set environment
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.2
```

## Common Dependencies

```bash
pip install ollama python-dotenv numpy
```

## Lessons Learned

These experiments taught key concepts:

1. **LLM API Patterns** - Consistent message formatting, temperature tuning
2. **RAG Architecture** - Embedding → Store → Retrieve → Generate
3. **Vector Databases** - FAISS indexing, similarity search, persistence
4. **Prompt Engineering** - System prompts, context injection, output formatting
5. **Security Applications** - MITRE ATT&CK integration, awareness content

---

*Part of the [myscripts](https://github.com/GLyttek/myscripts) collection*
