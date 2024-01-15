from fastapi import FastAPI
from enum import Enum
import typing as t

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}



@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id} 



class ModelName(str, Enum):
    ALEXNET = "ALEXNET"
    RESNET = "RESNET"
    LENET = "LENET"
    
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.ALEXNET:
        return {"model_name": model_name}
    
    elif model_name.value == "LENET":
        return {"model_name": model_name}
    
    else:
        return {"model_name": model_name}
    
    
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

dummy_db = [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10, optional_parameter: t.Optional[int] = None):
    return {
        'items': dummy_db[skip : skip + limit], 
        'optional_parameter': optional_parameter
    }

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: t.Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    
    if q:
        item.update({"q": q})
        
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
        
    return item


from pydantic import BaseModel


class Book(BaseModel):
    name : str
    author : str
    description : t.Optional[str] = None
    price: float
    
    
@app.post("/books/")
async def create_book(book: Book):
    return book