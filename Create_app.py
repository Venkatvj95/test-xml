import streamlit as st
from parser import parse_siplace_xml
from Create_rag import build_vector_db

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


st.set_page_config(
    page_title="SIPLACE Assistant",
    layout="wide"
)

st.title("SIPLACE Setup Assistant")

uploaded_file = st.file_uploader(
    "Upload SIPLACE XML",
    type=["xml"]
)

if uploaded_file:

    df = parse_siplace_xml(uploaded_file)

    st.subheader("Parsed Data")
    st.dataframe(df)

    empty_df = df[
        df["Component"] == "EMPTY"
    ]

    st.subheader("Empty Locations")
    st.dataframe(empty_df)

    st.success(
        f"Total Empty Locations : {len(empty_df)}"
    )

    vector_db = build_vector_db(df)

    llm = ChatOllama(
        model="llama3.2"
    )

    # Modern replacement for RetrievalQA
    prompt = ChatPromptTemplate.from_template("""
You are a SIPLACE machine setup assistant.
Use the following context to answer the question.

Context:
{context}

Question: {input}

Answer:""")

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    qa_chain = create_retrieval_chain(
        vector_db.as_retriever(),
        combine_docs_chain
    )

    question = st.chat_input(
        "Ask a question"
    )

    if question:

        response = qa_chain.invoke(
            {"input": question}   # changed from "query" to "input"
        )

        st.write(response["answer"])  # changed from "result" to "answer"
