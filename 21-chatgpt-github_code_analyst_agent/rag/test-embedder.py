from embedder import run_embedding_pipeline

code_files = [
    {"path": "example1.py", "code": "def hello():\n    print('Hello world')"},
    {"path": "example2.py", "code": "# just a comment\n"},
]

vectorstore = run_embedding_pipeline(code_files)
print("Embedding and storage done.")
