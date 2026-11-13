import pytest
from langchain_core.messages import AIMessage, HumanMessage

from memory import approximate_token_count, trim_history


def test_approximate_token_count_counts_words() -> None:
    messages = [HumanMessage(content="one two three"), AIMessage(content="four")]

    assert approximate_token_count(messages) == 6


def test_trim_history_keeps_recent_complete_turns() -> None:
    history = [
        HumanMessage(content="old question"),
        AIMessage(content="old answer"),
        HumanMessage(content="new question"),
        AIMessage(content="new answer"),
    ]

    assert trim_history(history, max_tokens=6) == history[-2:]


def test_trim_history_requires_a_positive_budget() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        trim_history([], max_tokens=0)
