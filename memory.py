"""Approximate token-budget trimming for an in-process chat history."""

import math
import re
from collections.abc import Sequence

from langchain_core.messages import BaseMessage
from langchain_core.messages.utils import trim_messages


def approximate_token_count(messages: Sequence[BaseMessage]) -> int:
    """Estimate tokens at 1.3 tokens per whitespace-delimited word."""
    text_parts = []
    for message in messages:
        content = message.content
        if isinstance(content, str):
            text_parts.append(content)
        else:
            text_parts.extend(
                block.get("text", "")
                for block in content
                if isinstance(block, dict) and isinstance(block.get("text"), str)
            )
    word_count = len(re.findall(r"\S+", " ".join(text_parts)))
    return math.ceil(word_count * 1.3)


def trim_history(
    messages: Sequence[BaseMessage],
    max_tokens: int,
) -> list[BaseMessage]:
    """Keep the most recent complete human-led exchanges within a budget."""
    if max_tokens < 1:
        raise ValueError("max_tokens must be greater than zero.")
    return trim_messages(
        list(messages),
        max_tokens=max_tokens,
        token_counter=approximate_token_count,
        strategy="last",
        start_on="human",
        include_system=False,
        allow_partial=False,
    )
