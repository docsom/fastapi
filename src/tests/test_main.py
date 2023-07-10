import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from api.main import app

# 테스트용 MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]
collection = db["test_collection"]

# 테스트 데이터 삽입
testdata = [
    {"id": "1", "name": "Item 1", "description": "Description 1"},
    {"id": "2", "name": "Item 2", "description": "Description 2"},
]
collection.insert_many(testdata)


# @pytest.fixture(scope="module")
# def event_loop():
#     # 테스트용 이벤트 루프 설정
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(scope="module")
# def test_app(event_loop):
#     # 테스트용 FastAPI 애플리케이션 설정
#     app.dependency_overrides[get_db] = get_test_db
#     yield app


# @pytest.fixture(scope="module")
# def test_db(event_loop):
#     # 테스트용 MongoDB 연결 설정
#     client = AsyncIOMotorClient("mongodb://localhost:27017/")
#     db = client["test_database"]
#     yield db
#     client.close()


# async def get_test_db():
#     # 테스트용 데이터베이스 세션 함수
#     yield test_db


# @pytest.mark.asyncio
# async def test_create_item(test_app, test_db):
#     # 항목 생성 테스트
#     item = {"id": "3", "name": "Item 3", "description": "Description 3"}
#     async with AsyncClient(app=test_app, base_url="http://test") as client:
#         response = await client.post("/items/", json=item)
#     assert response.status_code == 200
#     assert response.json() == item
#     assert await test_db.collection.count_documents({"id": "3"}) == 1


# @pytest.mark.asyncio
# async def test_read_items(test_app):
#     # 모든 항목 조회 테스트
#     async with AsyncClient(app=test_app, base_url="http://test") as client:
#         response = await client.get("/items/")
#     assert response.status_code == 200
#     assert len(response.json()) == 3


# @pytest.mark.asyncio
# async def test_read_item(test_app):
#     # 개별 항목 조회 테스트
#     async with AsyncClient(app=test_app, base_url="http://test") as client:
#         response = await client.get("/items/1")
#     assert response.status_code == 200
#     assert response.json()["id"] == "1"


# @pytest.mark.asyncio
# async def test_update_item(test_app, test_db):
#     # 항목 업데이트 테스트
#     item = {"id": "1", "name": "Updated Item", "description": "Updated Description"}
#     async with AsyncClient(app=test_app, base_url="http://test") as client:
#         response = await client.put("/items/1", json=item)
#     assert response.status_code == 200
#     assert response.json() == item
#     updated_item = await test_db.collection.find_one({"id": "1"})
#     assert updated_item["name"] == "Updated Item"


# @pytest.mark.asyncio
# async def test_delete_item(test_app, test_db):
#     # 항목 삭제 테스트
#     async with AsyncClient(app=test_app, base_url="http://test") as client:
#         response = await client.delete("/items/1")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Item deleted"}
#     assert await test_db.collection.count_documents({"id": "1"}) == 0
