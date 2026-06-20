import streamlit as st
from parser import parse_siplace_xml
from Create_rag import build_vector_db
from langchain_ollama import ChatOllama

st.set_page_config(page_title="SIPLACE Assistant", layout="wide")

st.title("SIPLACE Setup Assistant")

uploaded_file = st.file_uploader(
    "Upload SIPLACE XML",
    type=["xml"]
)

# Store current file name
if uploaded_file is not None:

    # Check if a new file was uploaded
    if (
        "current_file" not in st.session_state
        or st.session_state.current_file != uploaded_file.name
    ):

        st.session_state.current_file = uploaded_file.name

        # Parse latest XML
        df = parse_siplace_xml(uploaded_file)

        # Rebuild vector DB from latest XML
        st.session_state.df = df
        st.session_state.vector_db = build_vector_db(df)

        st.success(f"Loaded latest XML: {uploaded_file.name}")

# Display data if available
if "df" in st.session_state:

    df = st.session_state.df

    st.subheader("Parsed Data")
    st.dataframe(df)

    empty_df = df[df["Component"] == "EMPTY"]

    st.subheader("Empty Locations")
    st.dataframe(empty_df)

    st.success(f"Total Empty Locations: {len(empty_df)}")

    question = st.chat_input("Ask a question")

    if question:

        llm = ChatOllama(model="llama3.2")

        docs = st.session_state.vector_db.similarity_search(
            question,
            k=5
        )

        context = "\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are a SIPLACE machine setup assistant.

Context:
{context}

Question:
{question}

Answer:
"""

        response = llm.invoke(prompt)

        st.write(response.content)
