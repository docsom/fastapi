from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# MongoDB 클라이언트 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["items"]

# MongoDB 문서 모델 정의
class Item(BaseModel):
    id: str
    name: str
    description: str

@app.get("/")
def read_root():
    return {"Hello" : "World"}

# CRUD 엔드포인트 정의
@app.post("/items/")
def create_item(item: Item):
    item_data = item.dict()
    collection.insert_one(item_data)
    return item

@app.get("/items/")
def read_items():
    items = list(collection.find())
    return items

@app.get("/items/{item_id}")
def read_item(item_id: str):
    item = collection.find_one({"id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    item_data = item.dict()
    result = collection.update_one({"id": item_id}, {"$set": item_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    result = collection.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
