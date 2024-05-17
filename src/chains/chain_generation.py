from langchain.chains import RetrievalQAWithSourcesChain
from langchain.llms import OpenAI
from chains.retrieval_object import compresion_retriever_generation
from etl.embeddings import get_vectore_store_for_query
from templates.prompt_template import create_custom_prompt, create_custom_prompt_with_history, create_custom_prompt_with_history_i2
from memory.window_buffer_memory import create_window_buffer_memory

# load environment variables
from dotenv import load_dotenv
load_dotenv('../.env')
import asyncio


def chain_coupling():
    """
    This function generates the chain for the answering system.

    Args:
        None

    Returns:
        chain (RetrievalQAWithSourcesChain): chain for the answering system
    """
    # load vectorstore
    vector_store = get_vectore_store_for_query(index_name='mvp-test-hf4', model_embedding='hf', vector_store_client='deeplake')
    # create the retriever
    retriever = compresion_retriever_generation(vector_store, model_embedding='hf')
    # create the prompt
    prompt = create_custom_prompt()
    chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(
        temperature=0, model = "gpt-3.5-turbo-instruct"), chain_type="stuff", retriever=retriever, return_source_documents=False,
        chain_type_kwargs={"prompt": prompt}, return_only_outputs=False)
    return chain


async def chain_coupling_with_memory_deeplake():
    """
    This function generates the chain for the answering system considering the chat history.

    Args:
        None

    Returns:
        chain (RetrievalQAWithSourcesChain): chain for the answering system considering the chat history
    """
    a = asyncio.gather(get_vectore_store_for_query(index_name='mvp-test-hf4', model_embedding='hf', vector_store_client='deeplake'), create_custom_prompt_with_history_i2(), create_window_buffer_memory(length_history=3))
    # create the prompt
    vector_store, prompt, memory = await a
    retriever = await compresion_retriever_generation(vector_store, model_embedding='hf')
    chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0, model = "gpt-3.5-turbo-instruct"), chain_type="stuff", retriever=retriever,
                                                        memory=memory, return_source_documents=True, chain_type_kwargs={"prompt": prompt})
    return chain


async def chain_coupling_with_memory_pinecone():
    """
    This function generates the chain for the answering system considering the chat history.

    Args:
        None

    Returns:
        chain (RetrievalQAWithSourcesChain): chain for the answering system considering the chat history
    """
    a = asyncio.gather(get_vectore_store_for_query(index_name='mvp-test3', model_embedding='hf', vector_store_client='pinecone', namespace='hf-384'), create_custom_prompt_with_history_i2(), create_window_buffer_memory(length_history=3))
    # create the prompt
    vector_store, prompt, memory = await a
    retriever = await compresion_retriever_generation(vector_store, model_embedding='hf')
    chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0, model = "gpt-3.5-turbo-instruct"), chain_type="stuff", retriever=retriever,
                                                        memory=memory, return_source_documents=True, chain_type_kwargs={"prompt": prompt})
    return chain
