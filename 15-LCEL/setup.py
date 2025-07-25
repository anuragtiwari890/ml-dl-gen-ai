# serve_test.py
from fastapi import FastAPI
from langchain_core.runnables import RunnableLambda
from langserve import add_routes

def simple_func(inputs: dict) -> str:
    return f"Echo: {inputs['text']}"

chain = RunnableLambda(simple_func)

app = FastAPI()
add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
