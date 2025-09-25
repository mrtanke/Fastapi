from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi. encoders import jsonable_encoder

app = FastAPI()

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2, "tags": ["bar", "fighter"]},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
	stored_item_data = items[item_id]
	stored_item_model = Item(**stored_item_data)

	update_data = item.dict(exclude_unset=True)
	update_item = stored_item_model.copy_model(update=update_data)

	items[item_id] = jsonable_encoder(update_item)

	return update_item

'''
Partial update:
    1. Retrieve the stored data.
    2. Put the data in the Pydantic model.
    3. Generate a dict without default values from the input model.
    4. Create a new model by copying the stored model and updating it with the new data.
    5. Convert the updated model to JSON-compatible dict and store it.
    6. Save the data in ur DB.
    7. Return the updated model.
'''