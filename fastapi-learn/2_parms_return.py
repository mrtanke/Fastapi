from typing import Annotated, Any
from fastapi import FastAPI, Cookie, Header
from pydantic import BaseModel, EmailStr
from fastapi.responses import JSONResponse, RedirectResponse, Response

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude={"name", "description"}) # a set
async def read_item(item_id: str):
    return items[item_id]

'''
1. return value 
    response_model: 
        during runtime -> filter and validate return value during runtime
        doc generation -> generate JSON schema
    response_class -> package response by response_class during runtime
    (->) -> present openapi schema during document generation.
'''