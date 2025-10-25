import streamlit as st
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

# Page setup
st.set_page_config(page_title="TEG Chat Bot", page_icon="🤖", layout="centered")

# Title and bot doodle
col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712104.png", width=80)  # 🤖 bot doodle
with col2:
    st.markdown("<h1 style='margin-bottom:0;'>TEG Chat Bot</h1>", unsafe_allow_html=True)
    st.caption("Your friendly AI assistant powered by RAG")

st.divider()

# Load RAG components
@st.cache_resource
def init_rag():
    docs = load_all_documents("data")
    store = FaissVectorStore("faiss_store")
    store.build_from_documents(docs)
    rag_search = RAGSearch()
    return rag_search

rag_search = init_rag()

# Maintain chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat messages
for chat in st.session_state.history:
    if chat["role"] == "user":
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(chat["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(chat["content"])

# Input box
query = st.chat_input("Ask your question...")
if query:
    st.session_state.history.append({"role": "user", "content": query})

    # Display a temporary "thinking..." message
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking... 🤔"):
            summary = rag_search.search_and_summarize(query, top_k=3)
            st.markdown(summary)

    st.session_state.history.append({"role": "assistant", "content": summary})


# to activate envirnament " venv\Scripts\activate "
# to run chat bot " streamlit run app.py "
# for closing the chat bot press ctrl + c 