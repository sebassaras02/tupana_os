from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import Pinecone, DeepLake
import pinecone
import os
from dotenv import load_dotenv
from typing import List
import asyncio

load_dotenv('../.env')


async def generate_text_embeddings(text: str, model_embedding: str):
    """
    This function generates embeddings for a given text with the HuggingFace model through the inference API.

    Args:
        text (str or list): text to be embedded

    Returns:
        query_result (np.array): embeddings for the given text
    """
    # Select the embedding model
    if model_embedding == 'hf':
        embedding = HuggingFaceInferenceAPIEmbeddings(
            api_key=os.environ['HUGGINGFACE_INFERENCE_API_KEY'], model_name="intfloat/multilingual-e5-small"
        )
    elif model_embedding == 'openai':
        embedding = OpenAIEmbeddings()
    # Embed the text or list of texts
    if len(text) > 1:
        query_result = embedding.aembed_documents(text)
        return query_result
    elif len(text) == 1:
        query_result = embedding.aembed_query(text)
        return query_result
    else:
        pass


async def get_vectore_store_for_query(index_name: str, model_embedding: str, vector_store_client: str, namespace: str = None):
    """
    This function returns the vector store for the query.

    Args:
        index_name (str): name of the index of the pinecone vector db to connect to

    Returns:
        vector_store (Pinecone): vector store for the query
    """
    # Select the embedding model
    if model_embedding == 'hf':
        embedding = HuggingFaceInferenceAPIEmbeddings(
            api_key=os.environ['HUGGINGFACE_INFERENCE_API_KEY'], model_name="intfloat/multilingual-e5-small"
        )
    elif model_embedding == 'openai':
        embedding = OpenAIEmbeddings()
    # Select the vector store client
    if vector_store_client == 'pinecone':
        pinecone.init(api_key=os.environ["PINECONE_API_KEY"],
                      environment=os.environ["PINECONE_ENV"])
        vector_store = Pinecone.from_existing_index(
            index_name=index_name, embedding=embedding, namespace=namespace)
        return vector_store
    elif vector_store_client == 'deeplake':
        vector_store = DeepLake(
            dataset_path="hub://sebitasalejo/" + index_name, embedding=embedding)
        return vector_store


async def delete_all_vectors_from_db(index_name: str, model_embedding: str, vector_store_client: str, namespace: str = None):
    """
    This function deletes all vectors from the Pinecone vector db.

    Args:
        index_name (str): name of the index to be deleted

    Returns:
        None
    """
    # select the embedding model
    print("Choosing the embedding model...")
    if model_embedding == 'hf':
        embedding = HuggingFaceInferenceAPIEmbeddings(
            api_key=os.environ['HUGGINGFACE_INFERENCE_API_KEY'], model_name="intfloat/multilingual-e5-small"
        )
    elif model_embedding == 'openai':
        embedding = OpenAIEmbeddings()
    # select the vectoxr store client
    print("Choosing the vector store client...")
    if vector_store_client == 'pinecone':
        pinecone.init(api_key=os.environ["PINECONE_API_KEY"],
                      environment=os.environ["PINECONE_ENV"])
        vector_store = Pinecone.from_existing_index(
            index_name=index_name, embedding=embedding, namespace=namespace)
        vector_store.delete(delete_all=True, namespace=namespace)
    elif vector_store_client == 'deeplake':
        vector_store = DeepLake(
            dataset_path="index_name", embedding=embedding)
        vector_store.delete(delete_all=True)


async def push_vectors_from_docs(index_name: str, docs: List, model_embedding: str, vector_store_client: str, namespace: str = None):
    """
    This function pushes vectors from a list of documents to the Pinecone vector db.

    Args:
        index_name (str): name of the index to be deleted
        docs (list): list of documents

    Returns:
        None
    """
    print("Choosing the embedding model...")
    if model_embedding == 'hf':
        embedding = HuggingFaceInferenceAPIEmbeddings(
            api_key=os.environ['HUGGINGFACE_INFERENCE_API_KEY'], model_name="intfloat/multilingual-e5-small"
        )
    elif model_embedding == 'openai':
        embedding = OpenAIEmbeddings()
    print("Choosing the vector store client...")
    if vector_store_client == 'pinecone':
        pinecone.init(api_key=os.environ["PINECONE_API_KEY"],
                      environment=os.environ["PINECONE_ENV"])
        vectorstore = Pinecone.from_existing_index(
            index_name=index_name, embedding=embedding, text_key="text", namespace=namespace)
        await vectorstore.afrom_documents(
            index_name=index_name, documents=docs, embedding=embedding, namespace=namespace)
    elif vector_store_client == 'deeplake':
        await DeepLake.afrom_documents(
            documents=docs, dataset_path="hub://sebitasalejo/" + index_name, embedding=embedding)
