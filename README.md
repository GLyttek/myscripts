# myscripts — where my practical AI work began

This repository is a public record of scripts, examples, and small prototypes I published and used while learning how to work with language models.

It began on 2 March 2024 with a rough local-model comparison. A few weeks later I was calling Claude and Groq from Python, preserving a chatbot conversation in a list, transcribing audio with Whisper, and saving generated material as documents. The code is small and sometimes brittle. That is part of its value: it shows the distance between opening a chat window and learning what an API, a local model, a retrieval pipeline, or a tool-using agent actually requires.

This is a historical workshop, not one maintained application. The directories come from different periods and do not share one maturity level, dependency set, or security review.

The repository is not a claim that I wrote every line from scratch. Git history shows when material was published and which changes came through coding-agent branches. The mixed `llm-experiments/` collection still has no line-by-line provenance map, so I treat it as study material rather than a source library for reuse.

## Why I keep the early code public

An [early README from the first evening](https://github.com/GLyttek/myscripts/blob/43c48310932eda32b10d1b5e1db567dda5a33535/README.md) was already asking how to compare model output for accuracy, clarity, completeness, language, relevance, and formatting. The method was basic and no real benchmark followed from it, but the question survived.

Later work became more structured: file-based workers, approval queues, local and cloud model roles, Aletheia, agent experiments, and finally a maintained harness. The fuller record, including corrections and present limits, lives in the [Lyttek AI Journey](https://github.com/GLyttek/lyttek-ai-journey).

I do not want to rewrite these early scripts as if I had today's controls in 2024. Readers should be able to see what I used, what I understood at the time, and why later systems added stronger boundaries.

## Public timeline

| Public date | What appeared in this repository | What it represents |
|---|---|---|
| **2 March 2024** | [Local-model comparison through Ollama](https://github.com/GLyttek/myscripts/commit/080422481e981934c573f36fb41d3624aa7900d9) | My first public attempt to inspect model output for German cybersecurity tasks |
| **24 March 2024** | [Claude API document generation](https://github.com/GLyttek/myscripts/commit/0b19f0669b38ef0de03352d0a76de269122d5f00) | Moving from a chat interface to repeated API calls and saved artifacts |
| **3 April 2024** | [Groq/Mixtral terminal chatbot](https://github.com/GLyttek/myscripts/commit/ef2bffa9de363ee6660221c37c57d8fbef98e5ab) and [Whisper-based audio pipeline](https://github.com/GLyttek/myscripts/commit/50e128f7453da379feda240ead4cb633688394fd) | Conversation state, transcription, summarization, and chained model calls |
| **June 2025** | [Monitoring](https://github.com/GLyttek/myscripts/commit/b9716db627e1fe52d67a4a58e4dd9f3ed8e3bd67) and [network-analysis](https://github.com/GLyttek/myscripts/commit/1f27224773bad28bf49a1b5dc131bfe22f6719ac) prototypes | Larger application ideas, local inference, web interfaces, and the limits of generated scaffolds |
| **February 2026** | [`llm-experiments/` collection](https://github.com/GLyttek/myscripts/commit/e629107ee0d1a6ac51ca42f753b60773f82c8cca) and [later additions](https://github.com/GLyttek/myscripts/commit/9467f33605de0556d22befe8ff1c96573a48e782) | RAG, MITRE ATT&CK extraction, security-awareness generation, YouTube retrieval, and simple agent patterns gathered as learning material |

The current location of a file does not prove that the same file existed in an earlier period. Git history is the public chronology.

## Repository map

| Path | Role | Public provenance | Current status |
|---|---|---|---|
| [`scripts/`](scripts/) | Four early local-model, Claude, Groq, and Whisper utilities | Original files committed through this account in 2024; moved and documented through [PR #2](https://github.com/GLyttek/myscripts/pull/2) in 2025 | Historical learning scripts; useful for reading, not maintained as a supported package |
| [`monitoring-app/`](monitoring-app/) | FastAPI/React monitoring proof of concept with local Ollama analysis | Added through a Codex-named branch in [PR #1](https://github.com/GLyttek/myscripts/pull/1) | Prototype from 2025; requires security and compatibility review before any real deployment |
| [`network_analysis/`](network_analysis/) | Packet/flow-analysis scaffold with local-model classification hooks | Added through a Codex-named branch in [PR #5](https://github.com/GLyttek/myscripts/pull/5) | Minimal proof of concept; placeholder functions and privileged capture make it unsuitable as a deployment starting point |
| [`llm-experiments/`](llm-experiments/) | Mixed collection of retrieval, security, media, and agent experiments | Published in the linked February 2026 commits; no line-by-line source map established | Added publicly in 2026; not uniformly tested or reviewed |
| [`environment.yml`](environment.yml) | Shared Conda environment attempt | Added through a Codex-named branch in [PR #3](https://github.com/GLyttek/myscripts/pull/3) | Convenience file, not a reproducible guarantee for every subproject |

## The four original scripts

- [`claude_call.py`](scripts/claude_call.py) — calls Anthropic's API for sections of a document and saves DOCX and HTML output.
- [`groq_simple_chatbot.py`](scripts/groq_simple_chatbot.py) — keeps a small terminal conversation in memory and calls Groq.
- [`read_mp3_summary.py`](scripts/read_mp3_summary.py) — transcribes an MP3 with Faster Whisper and passes the result into Groq-based summarization steps.
- [`testing_local_model.py`](scripts/testing_local_model.py) — sends the same German cybersecurity tasks to two Ollama-backed model placeholders and saves their output.

See [`scripts/README.md`](scripts/README.md) for the basic setup expected by those files.

## Reading and running the repository

There is no repository-wide compatibility guarantee or supported release. If you run an example:

At the August 2026 review, the repository-wide GitHub Action reached Flake8 and failed because [`llm-experiments/youtube-rag/yt-rag.py`](llm-experiments/youtube-rag/yt-rag.py) references three undefined helper functions. The file is unchanged by this README update. The failed check confirms that the collection is not one supported package; it is not a failure I want to hide behind an archive label.

1. read the source and its local README first;
2. create an isolated environment rather than installing dependencies globally;
3. provide API keys through environment variables and never commit them;
4. use synthetic or public test data;
5. check local service bindings, authentication, file destinations, and model revisions;
6. treat generated classifications, summaries, and instructions as unverified output;
7. do not run packet-capture or monitoring examples with elevated privileges on a sensitive system without a separate review.

The root Conda file can be used as a starting point for the original scripts:

```bash
conda env create -f environment.yml
conda activate myscripts
```

Individual subprojects may need different or newer dependencies. Historical examples may no longer work unchanged against current APIs or models.

## Related

- [Lyttek AI Journey](https://github.com/GLyttek/lyttek-ai-journey) — the documented path from Pi and early chatbots through APIs, local models, Claude Code, custom workers, agent experiments, and a bounded human-approved harness.
- [Current State](https://github.com/GLyttek/lyttek-ai-journey/blob/main/CURRENT_STATE.md) — what remains active in August 2026 and which gaps are still open.
