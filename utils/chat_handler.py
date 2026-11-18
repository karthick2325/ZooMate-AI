
from utils.langchain_client import get_zoo_response


def chat_with_zoo_mate(user_message, chat_history=None):

    if not user_message or not user_message.strip():
        return "Please enter your question."

    response = get_zoo_response(
        question=user_message,
        chat_history=chat_history
    )

    return response
