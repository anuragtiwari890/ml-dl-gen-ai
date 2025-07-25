from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
from dotenv import load_dotenv
import uvicorn

import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

print(groq_api_key)

# Use a valid model for Groq
model=ChatGroq(model="llama-3.2-90b-vision-preview",groq_api_key=groq_api_key)

prompt_template = ChatPromptTemplate.from_messages([
    ('system', "Translate the following into {language}:"),
    ('user', '{text}')
])

parser = StrOutputParser()

chain = prompt_template | model | parser

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="LangChain API"
)

# Add routes with debug=True
add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
