from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict
from pydantic import BaseModel
import traceback
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
app = FastAPI()
load_dotenv()

mongo_db_url = os.getenv("URL")
def get_collection():
    client = AsyncIOMotorClient(mongo_db_url)  
    db = client["metadata"]  
    collection = db["metadata_collections"]  
    return collection

@app.on_event("startup")
async def startup_db_client():
    global client, db, collection
    client = AsyncIOMotorClient(mongo_db_url)  
    db = client["metadata"] 
    collection = db["metadata_collections"]
    # collection = get_collection()
    # await collection.create_index([("Title", "text"), ("SubCategory", "text")])
    # existing_indexes = await db["metadata_collections"].index_information()
    # print("Existing indexes:", existing_indexes)

@app.on_event("shutdown")
def shutdown_db_client():
    client.close()

class SimpleQuery(BaseModel):
    query: str

@app.post("/simple_search")
async def simple_search(q: SimpleQuery, collection=Depends(get_collection)):
    return await search_titles(q.query, collection)

@app.get("/search/", response_model=List[Dict])
async def search_titles(q: str, collection=Depends(get_collection)):
    words = q.split()
    filtered_words = [word for word in words if word.lower() not in ["the", "is", "in", "india"]]
    search_query = " ".join(filtered_words)
    cursor = collection.find({
        "$or": [
            {"Title": {"$regex": search_query, "$options": 'i'}},
            {"SubCategory": {"$regex": search_query, "$options": 'i'}}
        ]
    })
    result = []
    async for document in cursor:
        relevance = 0
        if not document.get("ParentExists"):
            relevance += 2
        elif document.get("Child"):
            relevance += 1
        elif document.get("ParentExists") and not document.get("Child"):
            relevance += 0.5

        if 'CPI' in document.get("Title"):
            relevance += 5

        simplified_document = {"Title": document["Title"], "Category": document["Category"], "SubCategory": document["SubCategory"], "relevance": relevance}
        result.append(simplified_document)

    result = sorted(result, key=lambda x: x["relevance"], reverse=True)
    return result

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    print(f"An error occurred: {exc}")
    traceback.print_exc()
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
