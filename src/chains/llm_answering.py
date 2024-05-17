from typing import Dict

def format_metadata(docs : Dict) -> str:
    """
    This function formats the metadata of the documents retrieved by the chain.

    Args:
        docs (dict): dictionary with the documents retrieved by the chain

    Returns:
        result (str): formatted metadata
    """
    metadata = [val.metadata for val in docs['source_documents']]
    compressed_data = {}

    for entry in metadata:
        source = entry['source']
        page = int(entry['page'])
        if source in compressed_data:
            if page not in compressed_data[source]['pages']:
                compressed_data[source]['pages'].append(page)
        else:
            compressed_data[source] = {'pages': [page]}
            
    result = "Los siguientes documentos se emplearon para contestar la pregunta:"

    for i, (source, info) in enumerate(compressed_data.items(), start=1):
        pages = ', '.join(map(str, sorted(list(info['pages']))))  # Convierte a lista y ordena las páginas
        result += f" Documento {i}: {source} en las páginas {pages}"

    return result


def llm_result(query : str, chain) -> str:
    """
    This function generates the answer for a query given by the user.

    Args:
        query (str): query given by the user
        chain (RetrievalQAWithSourcesChain): chain for the answering system

    Returns:
        response (str): answer for the query given by the user
    """
    res = chain({"question": query})
    if res['answer'] == ' No lo sé, no se encuentra en mi base de datos.':
        return res['answer']
    elif res['answer'] == ' Intento de hacking detectado.':
        return res['answer']
    # elif res['sources'] == "":
    #     return res['answer']
    else:
        metadata_info = format_metadata(res)
        final_response = f"{res['answer']}\n\n{metadata_info}"
        return final_response  

