from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    description: str

app = FastAPI()

client = AsyncIOMotorClient("mongodb+srv://152003harsh:7Zgy4F3JkTPqAcje@cluster0.sje4wcv.mongodb.net/?retryWrites=true&w=majority")
db = client["metadata"]
collection = db["metadata_collections"]

@app.on_event("startup")
async def startup_db_client():
    global client, db, collection
    client = AsyncIOMotorClient("mongodb+srv://152003harsh:7Zgy4F3JkTPqAcje@cluster0.sje4wcv.mongodb.net/?retryWrites=true&w=majority")
    db = client["metadata"]
    collection = db["metadata_collections"]

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

@app.post("/add/")
async def add_item(item: Item):
    item_dict = item.dict()
    await collection.insert_one(item_dict)
    return {"message": "Item inserted"}

@app.get("/items/", response_model=List[Item])
async def get_items():
    items = []
    async for item in collection.find():
        items.append(Item(**item))
    return items
