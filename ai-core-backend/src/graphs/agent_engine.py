from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from src.graphs.tools.finance_toolkit import finance_toolkit
from dotenv import load_dotenv
import os

load_dotenv()

# Groq Provider
groq_provider=ChatGroq(
  model=os.getenv("GROQ_MODEL_NAME"),
  api_key=os.getenv("GROQ_API_KEY"),
  temperature=0.7
)

# Local Ollama Provider
ollama_local_provider= ChatOllama(
  model=os.getenv("OLLAMA_MODEL_NAME"),
  temperature=0.7,
  base_url=os.getenv("OLLAMA_URL")
)

# Developer Provider selection

provider_choice = 2  # Change as needed: 1=Groq, 2=Ollama
match provider_choice:
    case 1:
        llm = groq_provider
    case 2:
        llm = ollama_local_provider
    case _:
        llm = groq_provider


Eth_L800_engine = llm.bind_tools(finance_toolkit)