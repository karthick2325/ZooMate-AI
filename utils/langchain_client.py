
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

from config import GEMINI_API_KEY
from prompts.system_prompt import SYSTEM_PROMPT


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GEMINI_API_KEY
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

output_parser = StrOutputParser()

zoo_chain = prompt | llm | output_parser


def get_zoo_response(question, chat_history=None):

    try:
        history = []

        if chat_history:
            for message in chat_history[-12:]:
                if message["role"] == "user":
                    history.append(HumanMessage(content=message["content"]))

                elif message["role"] == "assistant":
                    history.append(AIMessage(content=message["content"]))

        response = zoo_chain.invoke({
            "question": question,
            "chat_history": history
        })

        return response

    except Exception as e:
        return f"ZooMate AI Error: {str(e)}"
