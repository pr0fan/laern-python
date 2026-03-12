import pytest
from main import app
import asyncio
from httpx import AsyncClient, ASGITransport
from database import get_db
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture(scope="function")
async def test_db():
    MONGO_URL = "mongodb://localhost:27017"
    DB_NAME = "fitnesAppTest"
    APP_ENV = "prod"
    client = AsyncIOMotorClient(MONGO_URL)
    get_db = client[DB_NAME]
    yield get_db
    client.close()
    await asyncio.sleep(0)

@pytest.fixture(scope="function", autouse=True)
async def clear_db(test_db):
    await test_db.exercises.delete_many({})

@pytest.fixture(scope="function")
async def client(test_db):

    app.dependency_overrides[get_db] = lambda: test_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


async def test_root(client):
    response = await client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Python!"}

async def test_get_exercises_is_empty(client):
    response = await client.get("/exercises")
    
    assert response.status_code == 200
    assert response.json() == []

async def test_get_exercises_is_not_empty(client):
    post_response = await client.post(
        "/exercises", 
        headers={"X-Token": "coneofsilence"},
        json={"name": "test 1","weight": 10,"category": "test category"}
    )
    
    assert post_response.status_code == 200
    response = await client.get("/exercises")
    
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "test 1"
    assert data[0]["weight"] == 10
    assert data[0]["category"] == "test category"

async def test_get_exercises_summary(client):
    res_one = await client.post(
        "/exercises", 
        headers={"X-Token": "coneofsilence"},
        json={"name": "test 1","weight": 10,"category": "test category"}
    )
    
    res_two = await client.post(
        "/exercises", 
        headers={"X-Token": "coneofsilence"},
        json={"name": "test 2","weight": 20,"category": "test category 2"}
    )

    response = await client.get("/exercises/summary")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["max_weight"] == 20
    assert data["min_weight"] == 10
    assert data["average"] == 15.0

async def test_get_exercises_summary_if_not_exercises(client):
    response = await client.get("/exercises/summary")
    
    assert response.status_code == 400

async def test_get_exercises_heaviest(client):
    res_one = await client.post(
        "/exercises", 
        headers={"X-Token": "coneofsilence"},
        json={"name": "test 1","weight": 10,"category": "test category"}
    )
    
    res_two = await client.post(
        "/exercises", 
        headers={"X-Token": "coneofsilence"},
        json={"name": "test 2","weight": 20,"category": "test category 2"}
    )

    response = await client.get("/exercises/heaviest")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test 2"
    assert data["weight"] == 20
    assert data["category"] == "test category 2"

async def test_get_exercises_heaviest_if_not_exercises(client):
    response = await client.get("/exercises/heaviest")
    
    assert response.status_code == 400


#------------------------

async def test_get_exercises_by_category(client):
    res_one = await client.post(
        "/exercises", 
        headers={"X-Token": "coneofsilence"},
        json={"name": "test 1","weight": 10,"category": "test_category"}
    )
    
    res_two = await client.post(
        "/exercises", 
        headers={"X-Token": "coneofsilence"},
        json={"name": "test 2","weight": 20,"category": "test_category_2"}
    )

    res_three = await client.post(
        "/exercises", 
        headers={"X-Token": "coneofsilence"},
        json={"name": "test 3","weight": 30,"category": "test_category_2"}
    )

    response = await client.get("/exercises/test_category_2")
    
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "test 2"
    assert data[0]["weight"] == 20
    assert data[0]["category"] == "test_category_2"

    assert data[1]["name"] == "test 3"
    assert data[1]["weight"] == 30
    assert data[1]["category"] == "test_category_2"

async def test_get_exercises_by_category_if_not_exercises(client):
    response = await client.get("/exercises/test_category_2")
    
    assert response.status_code == 400

    