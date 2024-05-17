from text_splitter import create_text_chunks
from embeddings import push_vectors_from_docs


def pipeline_batch_processing_docs(path: str, index_name: str, model_embedding: str, vector_store_client: str):
    """
    This function takes a directory of pdf and word files, creates embeddings for each file, and push to a vectorial DB.

    Args:
        path: directory of pdf and word files
        model_embedding: embedding model to use
        vector_store_client: vector store client to use

    Returns:
        None
    """
    print("***************************************")
    print("Starting pipeline batch processing...")
    # create text chunks
    print("Starting text chunking...")
    texts = create_text_chunks(path)
    print("Finished text chunking...")
    print("***************************************")
    # push to vector store
    print("Starting pushing to vector store...")
    push_vectors_from_docs(index_name=index_name, docs=texts, model_embedding=model_embedding, vector_store_client=vector_store_client)
    print("Finished pushing to vector store...")
    print("***************************************")
    print("Finished pipeline batch processing...")
    return texts