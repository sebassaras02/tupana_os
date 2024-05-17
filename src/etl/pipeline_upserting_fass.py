from langchain.vectorstores import Pinecone, DeepLake
import pinecone
from dotenv import load_dotenv
import os
from embeddings import get_vectore_store_for_query
import asyncio

load_dotenv('../.env')


async def upsert_file_in_vector_store(index_name: str, vector_store_client: str, file_name: str, namespace: str = None):
    """
    This function deletes the vector store.

    Args:
        index _name (str): name of the index of the pinecone vector db to connect to
        vectore_store_client (str): vector store client to use
        file_name (str): name of the file to be deleted

    Returns:
        None
    """
    # Select the vector store client
    if vector_store_client == 'pinecone':
        pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment=os.environ["PINECONE_ENV"])
        vector_store = get_vectore_store_for_query(index=index_name, model_embedding='hf', vector_store_client=vector_store_client, namespace=namespace)
        await vector_store.aadd_documents(metadatas = file_name)
        
    elif vector_store_client == 'deeplake':
        vector_store = get_vectore_store_for_query(index=index_name, model_embedding='hf', vector_store_client=vector_store_client, namespace=namespace)
        await vector_store.aadd_documents(metadatas = file_name)
        
