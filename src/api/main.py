from jwt_manager import create_token
from fastapi import FastAPI, Depends, HTTPException
from models import ModelRequest, ModelResponse, User, VectorDBRequest, FileDBOps
from fastapi.responses import JSONResponse
import sys
import asyncio
from auth_val import JWTBearer

# load env variables
from dotenv import load_dotenv
load_dotenv('../../.env')

# import additional libraries
sys.path.append("../")
from chains.chain_generation import chain_coupling_with_memory_deeplake, chain_coupling_with_memory_pinecone

# start application
app = FastAPI()

############################################
#    AUTH OPERATIONS FOR  THE VECTOR STORE #
############################################

# define the login
@app.post("/login", tags=["AUTH"])
def login(user : User):
    if user.email == "sebastian.sarasti@tupana.com" and user.password == " admin123":
        token : str = create_token(user.dict())
    return token

############################################
#   INFERENCE    ENDPOINTS   FOR THE LLM   #
############################################

# create an event handler for the startup event
# @app.on_event("startup")
# async def startup_event():
#     app.state.chain = await chain_coupling_with_memory_deeplake()

# create an endpoint for the model
@app.post("/prediction_deeplake", tags=["INFERENCES"], response_model=ModelResponse, dependencies=[Depends(JWTBearer())])
async def get_llm_response(request: ModelRequest) -> ModelResponse:
    chain = await chain_coupling_with_memory_deeplake()
    request = request.dict()['question']
    answer = chain({"question": request})['answer']
    return ModelResponse(answer=answer)

@app.post("/prediction_pinecone", tags=["INFERENCES"], response_model=ModelResponse, dependencies=[Depends(JWTBearer())])
async def get_llm_response(request: ModelRequest) -> ModelResponse:
    chain = await chain_coupling_with_memory_pinecone()
    request = request.dict()['question']
    answer = chain({"question": request})['answer']
    return ModelResponse(answer=answer)


###########################################
# UPDATE OPERATIONS FOR THE VECTOR STORE  #
###########################################

@app.put("/update_file", tags=["UPDATE_OPS"], dependencies=[Depends(JWTBearer())])
async def update_file(request : FileDBOps) -> JSONResponse:
    from etl.pipeline_upserting_fass import upsert_file_in_vector_store
    index_name = request.index_name
    vector_store_client = request.vector_store_client
    namespace = request.namespace
    file_name = request.metadata
    upsert_file_in_vector_store(index_name=index_name, vector_store_client=vector_store_client, file_name=file_name, namespace=namespace)
    return JSONResponse(content={"message": "Item updated successfully"}, status_code=200)




###########################################
# DELETE OPERATIONS FOR THE VECTOR STORE #
###########################################

# create and endpoint to delete files in the vector store given the source of the file
@app.delete("/delete_all_files", tags=["DELETE_OPS"], dependencies=[Depends(JWTBearer())])
async def delete_all_files(request: VectorDBRequest) -> JSONResponse:
    from etl.embeddings import delete_all_vectors_from_db
    index_name = request.index_name
    model_embedding = request.model_embedding
    vector_store_client = request.vector_store_client
    namespace = request.namespace
    await delete_all_vectors_from_db(index_name = index_name, model_embedding = model_embedding, vector_store_client = vector_store_client, namespace = namespace)
    return JSONResponse(content={"message": "Vectorial database deleted successfully"}, status_code=200)

# create and endpoint to delete a file based on the metadata 
@app.delete("/delete_file_metadata", tags=["DELETE_OPS"], dependencies=[Depends(JWTBearer())])
async def delete_file_metadata(request: FileDBOps) -> JSONResponse:
    from etl.pipeline_deleting_fass import delete_file_in_vector_store
    index_name = request.index_name
    vector_store_client = request.vector_store_client
    namespace = request.namespace
    metadata = request.metadata
    await delete_file_in_vector_store(index_name = index_name, vector_store_client = vector_store_client, file_name = metadata, namespace = namespace)
    return JSONResponse(content={"message": "Item deleted successfully"}, status_code=200)