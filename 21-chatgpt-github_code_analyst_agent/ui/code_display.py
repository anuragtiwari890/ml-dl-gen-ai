import streamlit as st

def display_code(filename, code):
    with st.expander(f"📄 Code: {filename}", expanded=False):
        st.code(code, language='python')

def display_summary(summary):
    st.markdown("### 🧠 Summary")
    st.info(summary)

def loading_spinner():
    return st.spinner("Analyzing with LLM... please wait ⏳")
