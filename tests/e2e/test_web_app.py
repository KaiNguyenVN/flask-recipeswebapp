import pytest
from recipe import create_app
from flask import session

# ----------------- Authentication -----------------
def test_register_new_user(client):
    response = client.post("/authentication/register", data={
        "user_name": "testuser",
        "password": "Password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # redirected to login page


def test_register_duplicate_user(client):
    # First registration
    client.post("/authentication/register", data={
        "user_name": "dupuser",
        "password": "Password123"
    })
    # Duplicate attempt
    response = client.post("/authentication/register", data={
        "user_name": "dupuser",
        "password": "Password123"
    })
    assert b"already taken" in response.data


def test_login_success(client):
    # Register first
    client.post("/authentication/register", data={
        "user_name": "loginuser",
        "password": "Password123"
    })
    # Then login
    response = client.post("/authentication/login", data={
        "user_name": "loginuser",
        "password": "Password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"HOME" in response.data  # redirected home


def test_login_wrong_password(client):
    client.post("/authentication/register", data={
        "user_name": "badpass",
        "password": "Password123"
    })
    response = client.post("/authentication/login", data={
        "user_name": "badpass",
        "password": "WrongPass"
    })
    assert b"Password does not match" in response.data


def test_logout(client):
    client.post("/authentication/register", data={
        "user_name": "logoutuser",
        "password": "Password123"
    })
    client.post("/authentication/login", data={
        "user_name": "logoutuser",
        "password": "Password123"
    })
    response = client.get("/authentication/logout", follow_redirects=True)
    assert b"HOME" in response.data

# ----------------- post review -----------------
def test_post_review(client, auth, sample_recipe):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    r = client.post(
        f"/recipe/{sample_recipe.id}",
        data={
            "recipe_id": str(sample_recipe.id),
            "review_text": "So refreshing and easy!",
            "rating": "5",
            "submit": "Post Review",
        },
        follow_redirects=True,  # follow PRG redirect back to detail page
    )
    assert r.status_code == 200
    # optional: flash text
    assert b"Your review has been added!" in r.data
    # 5) Confirm review rendered on recipe page
    assert b"So refreshing and easy!" in r.data












"""
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
"""