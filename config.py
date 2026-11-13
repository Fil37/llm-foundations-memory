"""Environment-based local model configuration."""

import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama


load_dotenv()


def create_chat_model() -> ChatOllama:
    """Create the configured local chat model."""
    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "llama3.2"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0,
    )


def max_history_tokens() -> int:
    """Return a positive token budget for conversational history."""
    value = int(os.getenv("MAX_HISTORY_TOKENS", "388"))
    if value < 1:
        raise ValueError("MAX_HISTORY_TOKENS must be greater than zero.")
    return value
