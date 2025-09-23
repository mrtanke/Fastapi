from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, StringConstraints, AfterValidator, Field
from typing import Annotated, Literal
import random

app = FastAPI()

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item, 
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "description": "Invalid items will result in an error response",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            }
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results


'''
1. schema: template, like the application form, which u need to fill when u apply for a id card.
    Api schema: a blueprint for api request and response (interface function definition)
    Data schema: a blueprint for data structure (function data definition)
    OpenAPI and JSON schema: a blueprint for api content (api content definition)
2. Pydantic model: 
    => data schema
3. whole process:
    => request body => data schema(validation) => function processing 
    => response model(validation) => response body
4. POST, GET, PUT, DELETE
5. HTTP request
    - Request Line (Path, Query)
    - Headers (Cookie, Header)
    - Body (Body)
'''