from langchain.document_loaders import PyPDFLoader, DirectoryLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from typing import List

def clean_text(text : str) -> str:
    """
    This function cleans a given text by removing new lines, dots, multiple spaces and trailing spaces.

    Args:
        text (str): text to clean

    Returns:
        text (str): cleaned text
    """
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\.{3,}', '', text)
    text = re.sub(r'([^\w\s])\1{2,}', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"#\s*P\s*T\s*#", "", text)
    text = re.sub(r"\s*#", "", text)
    text = text.strip()
    return text

def generate_text_splitter():
    """
    This function generates a text splitter that splits a text into chunks of 600 characters with an overlap of 40 characters.
    
    Args:
        None
    
    Returns:
        splitter (RecursiveCharacterTextSplitter): text splitter
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=510, chunk_overlap=40, length_function=len, add_start_index=True, keep_separator = False)
    return splitter


def create_text_chunks(directory: str) -> List:
    """
    This function takes a directory of pdf files and creates embeddings for each pdf file.
    The embeddings are stored in a vector store. In a local file system where the script is executed

    Args:
        directory: directory of pdf files
        vector_store_name: name of the vector store to be created

    Return:
        texts (list): list of texts
    """
    print('loading pdfs...')
    loader = DirectoryLoader(path=directory, glob='**/*.pdf',
                             loader_cls=PyPDFLoader, use_multithreading=True)
    pdfs = loader.load()
    print('loading loaded...')

    print('loading words...')
    word_loader = DirectoryLoader(path=directory, glob='**/*.docx', loader_cls=UnstructuredWordDocumentLoader,
                                  use_multithreading=True, loader_kwargs={'mode': 'single'})
    word_docs = word_loader.load()
    print('words loaded...')

    # Combine docs
    docs = pdfs + word_docs
    
    # clean text before splitting
    print('cleaning texts...')
    for doc in docs:
        doc.page_content = clean_text(doc.page_content)
    print('text cleaned...')

    text_splitter = generate_text_splitter()
    texts = text_splitter.split_documents(docs)
    return texts
