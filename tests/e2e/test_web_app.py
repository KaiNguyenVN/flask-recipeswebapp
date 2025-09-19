import pytest
from recipe import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Home" in response.data
    assert b"Recipe" in response.data

def test_browse_page(client):
    response = client.get("/browse")
    assert response.status_code == 200
    assert b"browse-list" in response.data
    assert b"browse-card" in response.data

@pytest.mark.parametrize("recipe_id", [1, 2, 3])
def test_recipe_detail_page(client, recipe_id):
    response = client.get(f"/recipe/{recipe_id}")
    if response.status_code == 404:
        assert b"Recipe not found" in response.data
    else:
        assert response.status_code == 200
        assert b"Recipe" in response.data

def test_nonexistent_recipe(client):
    response = client.get("/recipe/99999")
    assert response.status_code == 404
    assert b"Recipe not found" in response.data

def test_log_in_required_to_comment(client):
    response = client.post("/recipe/comment")
    assert response.status_code == 401

def test_search_by_id(client):
    response = client.get("/search?recipe_id=45")
    assert response.status_code == 200
    assert b"applepie" in response.data

def test_rating(client, auth):
    auth.login()
    response = client.post("/recipe/rating")
    assert response.status_code == 200

def test_authentication(client):
    response = client.post("/login", data = {"username": "sid", "password": "123"})
    assert response.status_code == 200