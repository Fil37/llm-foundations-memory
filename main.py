"""Interactive local chat with bounded in-memory history."""

import os

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable

from config import create_chat_model, max_history_tokens
from memory import trim_history


SYSTEM_PROMPT = (
    "Tu es un assistant utile et concis. Réponds uniquement à partir du "
    "contexte fourni et signale clairement les incertitudes."
)
PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)


def create_chat_chain() -> Runnable:
    """Build the prompt/model chain used for each turn."""
    return PROMPT | create_chat_model()


def main() -> None:
    chain = create_chat_chain()
    history: list[HumanMessage | AIMessage] = []
    budget = max_history_tokens()
    print("Chat local démarré. Entrez 'exit' ou 'quit' pour arrêter.")

    while True:
        user_input = input("Vous : ").strip()
        if user_input.lower() in {"exit", "quit"}:
            return
        if not user_input:
            continue

        recent_history = trim_history(history, budget)
        response = chain.invoke({"history": recent_history, "input": user_input})
        answer = response.content
        if not isinstance(answer, str):
            raise TypeError("Le modèle a retourné un contenu non textuel.")
        print(f"Assistant : {answer}")
        history.extend([HumanMessage(content=user_input), AIMessage(content=answer)])


if __name__ == "__main__":
    main()
