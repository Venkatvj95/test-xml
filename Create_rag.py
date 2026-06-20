from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_vector_db(df):

    docs = []

    for _, row in df.iterrows():

        text = f"""
        Machine : {row['Machine']}
        Table : {row['Table']}
        Location : {row['Location']}
        Track : {row['Track']}
        Division : {row['Division']}
        Component : {row['Component']}
        """

        docs.append(
            Document(page_content=text)
        )

    embedding = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vector_db = FAISS.from_documents(
        docs,
        embedding
    )

    return vector_db