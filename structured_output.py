"""Pydantic-validated model output example."""

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from config import create_chat_model


class ReviewOutput(BaseModel):
    """Compact structured summary of written feedback."""

    summary: str = Field(description="A neutral summary of the feedback")
    positive_points: list[str] = Field(default_factory=list)
    improvement_points: list[str] = Field(default_factory=list)


def summarize_feedback(feedback: str) -> ReviewOutput:
    """Extract feedback into a validated structured response."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Résume le retour utilisateur sans ajouter de faits absents.",
            ),
            ("human", "{feedback}"),
        ]
    )
    chain = prompt | create_chat_model().with_structured_output(ReviewOutput)
    return chain.invoke({"feedback": feedback})
