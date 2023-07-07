from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, json
from motor.motor_asyncio import AsyncIOMotorClient

json.ENCODERS_BY_TYPE[ObjectId] = str
app = FastAPI()

# MongoDB 클라이언트 설정
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["items"]


# MongoDB 문서 모델 정의
class Item(BaseModel):
    id: str
    name: str
    description: str


@app.get("/")
async def read_root():
    return {"mesaage": "Hello, World!"}


# CRUD 엔드포인트 정의
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    item_data = item.dict()
    await collection.insert_one(item_data)
    return item


@app.get("/items/", response_model=list[Item])
async def read_items():
    items = await collection.find().to_list(length=None)
    return items


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    item = await collection.find_one({"id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    item_data = item.dict()
    result = await collection.update_one({"id": item_id}, {"$set": item_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await collection.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
