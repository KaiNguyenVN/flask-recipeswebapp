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

# ----------------- Search Test -----------------

def test_search_by_name(search_service):
    results = search_service.search_recipes(query="Chocolate", filter_by="name")
    assert results['total_recipes'] == 1
    assert results['recipes'][0].name == "Chocolate Cake"
    assert results['pagination']['page'] == 1
    assert results['pagination']['total_pages'] == 1

def test_search_by_ingredients(search_service):
    results = search_service.search_recipes(query="chicken", filter_by="ingredients")
    assert results['total_recipes'] == 1
    assert results['recipes'][0].name == "Salad Bowl"

def test_search_pagination(search_service):
    results = search_service.search_recipes(per_page=2, page=1)
    assert results['total_recipes'] == 3
    assert len(results['recipes']) == 2
    assert results['pagination']['total_pages'] == 2

def test_search_suggestions(search_service):
    results = search_service.search_recipes()
    assert "Chocolate Cake" in results['suggestions']['names']
    assert "Dessert" in results['suggestions']['categories']
    assert "Main Course" in results['suggestions']['categories']
    assert "Chef John" in results['suggestions']['authors']
    assert "flour" in results['suggestions']['ingredients']

def test_search_route_integration(client):
    response = client.get("/search?q=chicken")
    assert response.status_code == 200
    assert b"Search Results" in response.data

def test_search_with_filter(client):
    response = client.get("/search?q=cake&filter_by=name")
    assert response.status_code == 200

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

def test_search_pagination_route(client):
    response = client.get("/search?page=2")
    assert response.status_code == 200

def test_nutrition_data_included(search_service):
    results = search_service.search_recipes()
    for recipe in results['recipes']:
        assert recipe.id in results['nutrition']
        assert recipe.id in results['health_stars']

# ----------------- Health Star Rating Test -----------------

def test_health_stars_calculation(sample_nutrition):
    # Use the fixture nutrition object
    stars = sample_nutrition.calculate_health_stars()
    assert stars is not None

def test_health_stars_edge_cases(edge_sample_nutrition):
    stars = edge_sample_nutrition.calculate_health_stars()
    assert stars >= 0  # Should handle edge case without errors

def test_nutrition_properties(full_recipe):
    # Test the properties from the fixture
    nutrition = full_recipe
    assert nutrition.id == 1
    assert nutrition.calories == 300
    assert nutrition.fat == 10.5
    assert nutrition.saturated_fat == 3.2
    assert nutrition.protein == 15.0

def test_health_stars_unhealthy_recipe(unhealthy_recipe):
    stars = unhealthy_recipe.calculate_health_stars()
    assert stars == 0.5  # Should be min rating

def test_health_stars_mixed_recipe(mixed_recipe):
    stars = mixed_recipe.calculate_health_stars()
    assert stars == 1.0  # Should be low rating

def test_health_stars_medium_recipe(medium_recipe):
    stars = medium_recipe.calculate_health_stars()
    assert 3.0 <= stars <= 5.0

def test_health_stars_calculation_debug(nutrition_factory):
    # Test each component to understand scoring
    values = [0.5, 2.0, 4.0, 6.0]
    for i, sat_fat in enumerate(values, start=1):
        nutrition = nutrition_factory(recipe_id=i, saturated_fat=sat_fat)
        print(f"Sat fat {sat_fat}: {nutrition.calculate_health_stars()}")

def test_health_stars_missing_data(nutrition_factory):
    nutrition = nutrition_factory(recipe_id=4, saturated_fat=2.0, sugar=8.0)
    stars = nutrition.calculate_health_stars()
    assert stars is not None

def test_nutrition_equality(nutrition_factory):
    nutrition1 = nutrition_factory(1, calories=100, protein=10)
    nutrition2 = nutrition_factory(1, calories=100, protein=10)
    nutrition3 = nutrition_factory(2, calories=200, protein=20)

    assert nutrition1 == nutrition2
    assert nutrition1 != nutrition3


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