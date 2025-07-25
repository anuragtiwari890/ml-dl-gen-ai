'''
✅ Purpose:
    Defines a LangChain LLMChain that takes in a code snippet and outputs a summary.
'''
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama  # ✅ correct import

def build_code_summary_chain():
    prompt = PromptTemplate(
        input_variables=["code_snippet", "file_name"],
        template="""
You are a senior software engineer. Summarize the purpose and logic of this code file in short: {file_name}

Code:
{code_snippet}

Your detailed summary:
"""
    )
    llm = ChatOllama(model="phi3", temperature=0.3)
    return LLMChain(llm=llm, prompt=prompt)




'''
| Temperature | Behavior                           | Use Case                            |
| ----------- | ---------------------------------- | ----------------------------------- |
| `0.0`       | Deterministic, repeats same output | **Code generation**, factual tasks  |
| `~0.3`      | Low randomness                     | **Summarization, code explanation** |
| `0.7`       | Balanced randomness                | Chatbots, creative assistants       |
| `> 1.0`     | Highly random, varied responses    | Poetry, ideation, character agents  |

'''


'''
Summary - 
| Term              | Meaning                                                   |
| ----------------- | --------------------------------------------------------- |
| `temperature`     | Controls how deterministic or creative the output is      |
| `input_variables` | Dynamic fields used in your prompt                        |
| `PromptTemplate`  | Defines your prompt logic with variables                  |
| `LLMChain`        | Binds model + prompt into a callable chain                |
| `ChatOllama`      | Connects LangChain to local LLMs, customizable via params |

'''