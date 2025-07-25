## RAG Q&A Conversation With PDF Including Chat History

# Import necessary libraries
import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set HuggingFace token from environment
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")

# Load HuggingFace embeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Set up Streamlit UI
st.title("Conversational RAG With PDF uploads and chat history")
st.write("Upload PDFs and chat with their content")

# Input Groq API key (used to initialize the LLM)
api_key = st.text_input("Enter your Groq API key:", type="password")

# Proceed only if Groq API key is provided
if api_key:
    # Initialize Groq LLM with provided key and selected model
    llm = ChatGroq(groq_api_key=api_key, model_name="Gemma2-9b-It")

    # Text input for session ID to manage conversation history
    session_id = st.text_input("Session ID", value="default_session")

    # Initialize session-based storage if not present
    if 'store' not in st.session_state:
        st.session_state.store = {}

    # Upload one or more PDF files
    uploaded_files = st.file_uploader("Choose A PDF file", type="pdf", accept_multiple_files=True)

    # Process uploaded PDFs
    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            # Save the uploaded file temporarily
            temppdf = f"./temp.pdf"
            with open(temppdf, "wb") as file:
                file.write(uploaded_file.getvalue())
                file_name = uploaded_file.name

            # Load and extract content from PDF
            loader = PyPDFLoader(temppdf)
            docs = loader.load()
            documents.extend(docs)

        # Split long texts into chunks for vector storage
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)

        # Create Chroma vector store using document chunks and embeddings
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever()

        # Prompt to convert user queries into standalone questions using chat history
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )

        # Create a prompt template for question contextualization
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # Create retriever that uses history-aware question reformulation
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

        # Prompt for final answer generation using retrieved context
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )

        # Create the answer generation prompt template
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # Create a QA chain that uses the prompt and LLM
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        # Combine history-aware retriever and QA chain into a full RAG chain
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        # Function to retrieve or create session-based message history
        def get_session_history(session: str) -> BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                st.session_state.store[session_id] = ChatMessageHistory()
            return st.session_state.store[session_id]

        # Wrap the RAG chain with chat history memory
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        # Input field for user's question
        user_input = st.text_input("Your question:")

        if user_input:
            # Get current session history
            session_history = get_session_history(session_id)

            # Invoke the RAG pipeline with user input
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={
                    "configurable": {"session_id": session_id}
                },
            )

            # Show assistant response
            st.write(st.session_state.store)
            st.write("Assistant:", response['answer'])

            # Display full chat history
            st.write("Chat History:", session_history.messages)

# Display a warning if API key is not entered
else:
    st.warning("Please enter the Groq API Key")
