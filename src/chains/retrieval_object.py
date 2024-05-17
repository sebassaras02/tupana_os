from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings, OpenAIEmbeddings
import os
from dotenv import load_dotenv
import asyncio

load_dotenv('../.env')

async def compresion_retriever_generation(vectorstore, model_embedding='hf'):
    """
    This function takes a vector store and creates a compression retriever.
    
    Args:
        vectorstore: vector store to be compressed
        
    Returns:
        compression_retriever: compression retriever
    """
    if model_embedding == 'hf':
        embedding = HuggingFaceInferenceAPIEmbeddings(api_key=os.environ['HUGGINGFACE_INFERENCE_API_KEY'], model_name="intfloat/multilingual-e5-small")
    elif model_embedding == 'openai':
        embedding = OpenAIEmbeddings()
    embeddings_filter = EmbeddingsFilter(embeddings=embedding, similarity_threshold=0.75)
    retriever = vectorstore.as_retriever()
    compression_retriever = ContextualCompressionRetriever(base_compressor=embeddings_filter, base_retriever=retriever)
    return compression_retriever