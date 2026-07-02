# CLI Chatbot — Stateful Streaming Chat with a Local LLM

A command-line chatbot that holds a multi-turn conversation with a locally hosted
open-source language model, streaming replies token-by-token. Built as **Stage 0**
of my AI Engineering Roadmap — the foundational project for understanding how you
actually talk to an LLM from code.

Runs fully **offline and free** using [Ollama](https://ollama.com), with no API key
and no per-token cost.

---

## What it demonstrates

- **Messages & roles** — a conversation is a list of `system` / `user` / `assistant`
  messages, not a single blob of text.
- **Statelessness & memory** — the model remembers nothing on its own; the full
  history is resent on every request to preserve context.
- **Streaming** — responses are rendered incrementally as `delta` chunks arrive,
  for a responsive typing effect, while being accumulated to persist the full reply.
- **Robustness** — control commands (`exit`, `reset`) and error handling that keeps
  conversation history consistent when a request fails.
- **Provider-agnostic design** — uses the OpenAI-compatible API, so the same code
  runs against a hosted cloud model by changing only the endpoint and model name.

---

## Tech stack

- Python 3
- [Ollama](https://ollama.com) (local open-source model runtime)
- `openai` Python SDK (pointed at Ollama's OpenAI-compatible endpoint)

---

## Prerequisites

1. [Install Ollama](https://ollama.com).
2. Pull a model (a small one runs on most laptops):
   ```bash
   ollama pull llama3.2
   ```
3. Make sure the Ollama app/server is running.

---

## Setup & run

```bash
# clone and enter the project
git clone https://github.com/golamrasul97/01-cli-chatbot.git
cd cli-chatbot

# create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run
python chatbot.py
```

**Commands inside the chat:**
- `exit` — quit
- `reset` — clear the conversation and start fresh

---

## How it works

Each turn, the program appends your message to a running `messages` list and sends
the **entire list** to the model. Because the model is stateless, this resending is
what creates "memory." The reply streams back in small pieces, which are printed live
and concatenated into the full text — which is then appended back to `messages` so the
next turn has full context.

---

## Switching to a cloud model

Because Ollama uses the OpenAI-compatible format, moving to a hosted provider takes
three small changes and **no rewrite**: set `base_url` to the provider's endpoint,
supply a real `api_key`, and set `MODEL` to a hosted model name.

---

*Part of my [AI Engineering Roadmap](https://github.com/golamrasul97/ai-engineering-roadmap) — a build-in-public series pairing each concept
with a project you can build yourself.*