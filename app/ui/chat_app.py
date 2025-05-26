import streamlit as st
from app.pipeline.rag_chain import RAGPipeline

# Initialize RAG
rag = RAGPipeline()

st.set_page_config(page_title="Mortgage RAG Chat", layout="wide")
st.title("💬 Freddie Mac & Fannie Mae RAG Assistant")

# Session state to keep chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_input = st.text_input("Ask your question:", key="input")

if user_input:
    with st.spinner("Generating answer..."):
        answer = rag.query(user_input)
        st.session_state.history.append((user_input, answer))

# Display chat history
for question, response in reversed(st.session_state.history):
    st.markdown(f"**🧠 You:** {question}")
    st.markdown(f"**🤖 RAG:** {response}")
    st.markdown("---")
