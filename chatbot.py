"""
CLI Chatbot — a stateful, streaming chat client for a local LLM.

Connects to a locally hosted open-source model via Ollama's
OpenAI-compatible API. Maintains conversation history across turns
and streams responses token-by-token.

Prerequisites:
    - Ollama installed and running
    - Model pulled, e.g.: ollama pull llama3.2

Usage:
    python chatbot.py
    Commands: 'exit' to quit, 'reset' to clear the conversation.
"""

from openai import OpenAI

# Ollama exposes an OpenAI-compatible endpoint; api_key is required but unused locally.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama", # any string will work, but it must be non-empty to satisfy the OpenAI client
)
MODEL = "llama3.2"

SYSTEM_PROMPT = "You are a friendly, concise tutor."

# Conversation history. The model is stateless, so the full list is
# resent on every request to preserve context across turns.
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("Chatbot ready. Type 'exit' to quit, 'reset' to clear the conversation.\n")

while True:
    user_input = input("You: ")

    # Handle control commands before dispatching to the model.
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    if user_input.lower() == "reset":
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        print("Conversation cleared.\n")
        continue

    messages.append({"role": "user", "content": user_input})

    try:
        # Request a streamed completion so output can be rendered incrementally.
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
        )

        # Render each delta as it arrives while accumulating the full reply,
        # which is needed to persist the turn in history.
        print("Bot: ", end="", flush=True)
        reply = ""
        for chunk in stream:
            piece = chunk.choices[0].delta.content
            if piece is not None:
                print(piece, end="", flush=True)
                reply += piece
        print("\n")

        messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        # On failure, roll back the unanswered user message to keep history consistent.
        print(f"\n[Error talking to the API: {e}]\n")
        messages.pop()
        continue