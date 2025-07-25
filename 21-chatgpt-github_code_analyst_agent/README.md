# 🤖 ChatGPT GitHub Code Analyst Agent

A practical project demonstrating how to build an AI-powered agent that analyzes GitHub repositories using ChatGPT and related LLM technologies. This agent can summarize code, answer questions about codebases, and provide insights for developers.

---

## 📦 Features

| Feature                        | Description |
|-------------------------------|-------------|
| ✅ GitHub repo analysis        | Analyze and summarize code from public repositories |
| ✅ ChatGPT integration         | Use OpenAI's GPT models for code understanding |
| ✅ Q&A interface               | Ask questions about code structure, logic, and usage |
| ✅ File and function summaries | Get concise explanations for files and functions |
| ✅ Terminal/CLI interface      | Interact with the agent via command line |
| ✅ Extensible                  | Easily add new analysis or reporting features |

---

## 📁 Project Structure
<pre>├── app.py                  # Main entry point for the CLI agent
├── github_agent/           # Core logic for GitHub analysis and LLM integration
│   ├── fetch_repo.py       # Clones and fetches GitHub repositories
│   ├── code_parser.py      # Parses code files and extracts structure
│   ├── chatgpt_client.py   # Handles communication with OpenAI API
│   └── analysis.py         # Implements code analysis and Q&A logic
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment file for API keys
└── cloned_repos/           # Directory for cloned GitHub repositories
</pre>

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
python -m venv code-agent-env
source code-agent-env/bin/activate
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and add your OpenAI API key and any other required variables:

```bash
cp .env.example .env
# Edit .env and add your keys
```

### 3. Run the Agent

```bash
python app.py
```

---

## 🧰 Internals Explained

- **GitHub Integration**: Clones and parses public repositories for analysis.
- **LLM Analysis**: Uses ChatGPT to summarize code, answer questions, and provide insights.
- **Extensible Design**: Modular codebase for adding new features or analysis types.

---

## 📚 Learning Objectives

- Learn how to combine LLMs with code parsing for practical developer tools
- Understand the workflow for analyzing large codebases with AI
- Build a foundation for more advanced code assistants or documentation bots

---

## 📦 Requirements

- Python 3.9+
- openai
- requests
- gitpython
- python-dotenv

See `requirements.txt` for the full list.

---

## 🧑‍💻 Author & License

Built by Anurag Tiwari for hands-on learning with GenAI and code analysis.  
Feel free to fork, clone, and extend for your own projects.  
**License: MIT**
