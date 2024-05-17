from pydantic import BaseModel

class ModelRequest(BaseModel):
    question: str

class ModelResponse(BaseModel):
    answer: str

class User(BaseModel):
    email: str
    password: str
    
class VectorDBRequest(BaseModel):
    index_name: str
    model_embedding: str
    vector_store_client: str
    namespace: str = None
    
class FileDBOps(BaseModel):
    index_name: str
    vector_store_client: str
    namespace: str = None
    metadata: str