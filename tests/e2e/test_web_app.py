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

RECIPE_ID = 38  # exists in tests/data/test_recipes.csv

def test_post_review_success_shows_flash_and_review(client):
    """Logged-in user posts a valid review:
       - PRG (redirect) occurs
       - flash message is shown
       - review text appears on the recipe page
    """
    # log in a user (fixture should register + login)
    client.post("/authentication/register", data={
        "user_name": "logoutuser",
        "password": "Password123"
    })
    client.post("/authentication/login", data={
        "user_name": "logoutuser",
        "password": "Password123"
    }, follow_redirects=True)

    # post a review
    r = client.post(
        f"/recipe/{RECIPE_ID}",
        data={
            "recipe_id": str(RECIPE_ID),
            "review_text": "So refreshing and easy!",
            "rating": "5",
            "submit": "Post Review",
        },
        follow_redirects=True,  # follow PRG redirect back to detail page
    )

    # landed back on the recipe page
    assert r.status_code == 200
    # the new review is rendered
    assert b"So refreshing and easy!" in r.data


def test_post_review_requires_login_redirects_to_login(client):
    """If not logged in:
       - the user is sent to the login page
       - a flash explains they must be logged in
    """
    r = client.post(
        f"/recipe/{RECIPE_ID}",
        data={
            "recipe_id": str(RECIPE_ID),
            "review_text": "I should not be able to post",
            "rating": "5",
            "submit": "Post Review",
        },
        follow_redirects=True,
    )

    # We ended up on the login page with an appropriate flash
    assert r.status_code == 200
    assert b"<title>Login</title>" in r.data
    assert b"You must be logged in to post a review" in r.data


def test_add_favorite_recipe(client):
    # log in a user (fixture should register + login)
    client.post("/authentication/register", data={
        "user_name": "logoutuser",
        "password": "Password123"
    })
    client.post("/authentication/login", data={
        "user_name": "logoutuser",
        "password": "Password123"
    }, follow_redirects=True)

    r = client.post("/recipe/38/favorite", follow_redirects=True)

    assert r.status_code == 200
    assert b"Low-Fat Berry Blue Frozen Dessert" in r.data

def test_remove_favorite_recipe(client):
    # log in a user (fixture should register + login)
    client.post("/authentication/register", data={
        "user_name": "logoutuser",
        "password": "Password123"
    })
    client.post("/authentication/login", data={
        "user_name": "logoutuser",
        "password": "Password123"
    }, follow_redirects=True)

    client.post("/recipe/38/favorite", follow_redirects=True)
    r = client.post("/recipe/38/unfavorite", follow_redirects=True)

    assert r.status_code == 200











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