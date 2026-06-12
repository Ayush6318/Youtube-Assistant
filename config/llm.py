from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm():

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash"
    )

    return llm