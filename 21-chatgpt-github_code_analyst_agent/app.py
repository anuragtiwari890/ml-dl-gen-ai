import streamlit as st
import os

from tools.clone_repo import clone_repo, get_repo_files, read_file_content
from rag.rag_chain import answer_question_with_rag

# --- Page Config ---
st.set_page_config(page_title="GitHub Code Analyst", layout="wide")

st.title("🤖 GitHub Code Analyst (RAG + Ollama)")
st.write("Analyze code in a GitHub repo using Retrieval-Augmented Generation (RAG) powered by Ollama!")

# --- Input Section ---
repo_url = st.text_input("🔗 Enter GitHub repo URL (public):", placeholder="https://github.com/owner/repo")

if repo_url:
    # --- Clone Once Logic ---
    if "repo_path" not in st.session_state or st.session_state.repo_url != repo_url:
        with st.spinner("🔄 Cloning repo..."):
            try:
                repo_path = clone_repo(repo_url)
                st.session_state.repo_path = repo_path
                st.session_state.repo_url = repo_url
                st.success("✅ Repo cloned successfully.")
            except Exception as e:
                st.error(f"❌ Error cloning repo: {e}")
                st.stop()
    else:
        repo_path = st.session_state.repo_path
        st.info("📁 Repo already cloned. Using cached version.")

    st.write(f"📁 Local path: `{repo_path}`")

    # --- File Selection ---
    files = get_repo_files(repo_path)
    selected_file = st.selectbox("📄 Select a file to view:", files)

    if selected_file:
        file_content = read_file_content(repo_path, selected_file)

        # --- Display File Content (Collapsible) ---
        with st.expander("📜 View Code (click to expand)"):
            st.code(file_content, language="python")

        # --- Ask Questions ---
        user_query = st.text_input("Ask a question about this repo")

        if st.button("Generate Answer"):
            if user_query and selected_file:
                file_content = read_file_content(repo_path, selected_file)
                file_name = os.path.basename(selected_file)
                answer = answer_question_with_rag(user_query, file_content, selected_file)

                st.markdown("### 💬 Answer")
                st.write(answer)
