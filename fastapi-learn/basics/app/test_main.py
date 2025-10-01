from fastapi import FastAPI
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

# Test @app.get("/items/{item_id}", response_model=Item)
def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo", 
        "title": "Foo", 
        "description": "There goes my hero",
    }

def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hello"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid X-Token header"
    }

def test_read_noexistent_item():
    response = client.get("/items/reven", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Item not found"
    }

# Test @app.post("/items/", response_model=Item)
def test_create_item():
    response = client.post(
        "/items", 
        headers={"X-Token": "coneofsilence"},
        json={"id": "reven", "title": "master", "description": "a motivated student"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "reven", 
        "title": "master", 
        "description": "a motivated student"
    }

def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hello"},
        json={"id": "reven", "title": "master", "description": "a motivated student"}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid X-Token header"
    }

def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foo", "title": "Foo", "description": "There goes my hero"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}