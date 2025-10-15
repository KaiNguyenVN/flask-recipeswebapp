from datetime import datetime

import pytest
from pathlib import Path
from recipe import create_app
from recipe.adapters.memory_repository import MemoryRepository
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User
from recipe.search_function.services import SearchService
from recipe.adapters.repository_populate import populate

#from utils import get_project_root

TEST_DATA_PATH =  Path('./tests/data/test_recipes.csv')

@pytest.fixture
def repo():
    return MemoryRepository()


@pytest.fixture
def sample_user():
    return User("alice", "Password123", 1)


@pytest.fixture
def sample_recipe():
    return Recipe(38, "Low-Fat Berry Blue Frozen Dessert", Author(1533, "Dancer"))


@pytest.fixture
def sample_category():
    return Category("Italian")


@pytest.fixture
def sample_author():
    return Author(1, "Chef John")


@pytest.fixture
def sample_review(sample_user, sample_recipe):
    # Make sure username and recipe_id align with repo expectations
    return Review(
        sample_user.username,
        sample_recipe.id,
        5,
        "Great!",
        datetime.now(),
        1
    )

@pytest.fixture
def sample_nutrition():
    return Nutrition(1, 100, 10, 20, 30, 50, 60, 5, 10, 15)

@pytest.fixture
def edge_sample_nutrition():
    return Nutrition(2, 0, 0, 0, 0, 0, 0, 0, 0, 0)


@pytest.fixture
def sample_favourite(sample_user, sample_recipe):
    return Favourite(
        sample_user.username,
        sample_recipe,
        1
    )


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(Path('tests/data/test_recipes.csv'), repo, False)
    return repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='thorke', password='cLQ^C#oFXloS'):
        # Register first
        self.__client.post("/authentication/register", data={
            "user_name": user_name,
            "password": password
        })
        self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self.__client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)


@pytest.fixture
def authors_and_categories():
    author1 = Author(1, "Chef John")
    author2 = Author(2, "Mary Berry")
    category1 = Category("Dessert", [], 1)
    category2 = Category("Main Course", [], 2)
    return author1, author2, category1, category2

@pytest.fixture
def recipes(authors_and_categories):
    author1, author2, category1, category2 = authors_and_categories
    nutrition1 = Nutrition(1, calories=300, fat=10, saturated_fat=2, sugar=8, sodium=150, fiber=3, protein=12)
    nutrition2 = Nutrition(2, calories=500, fat=25, saturated_fat=8, sugar=25, sodium=800, fiber=1, protein=8)
    nutrition3 = Nutrition(3, calories=200, fat=5, saturated_fat=1, sugar=3, sodium=100, fiber=5, protein=15)

    recipes = [
        Recipe(
            recipe_id=1,
            name="Chocolate Cake",
            author=author1,
            category=category1,
            ingredients=["flour", "sugar", "chocolate"],
            nutrition=nutrition1
        ),
        Recipe(
            recipe_id=2,
            name="Beef Stew",
            author=author2,
            category=category2,
            ingredients=["beef", "carrot", "potato"],
            nutrition=nutrition2
        ),
        Recipe(
            recipe_id=3,
            name="Salad Bowl",
            author=author1,
            category=category2,
            ingredients=["lettuce", "tomato", "chicken"],
            nutrition=nutrition3
        ),
    ]

    return recipes

@pytest.fixture
def mock_repo(recipes):
    # A lightweight mock repository that returns predefined recipes and nutrition data.
    class Repo:
        def get_recipes(self):
            return recipes

        def get_nutrition_by_recipe_id(self, recipe_id):
            return next((r.nutrition for r in recipes if r.id == recipe_id), None)

    return Repo()

@pytest.fixture
def search_service(mock_repo):
    return SearchService(mock_repo)


@pytest.fixture
def unhealthy_recipe():
    return Nutrition(
        id=2,
        saturated_fat=10.0,
        sugar=25.0,
        sodium=800.0,
        fiber=0.5,
        protein=3.0
    )

@pytest.fixture
def mixed_recipe():
    return Nutrition(
        id=3,
        saturated_fat=3.0,
        sugar=12.0,
        sodium=300.0,
        fiber=3.0,
        protein=8.0
    )

@pytest.fixture
def medium_recipe():
    return Nutrition(
        id=4,
        saturated_fat=2.0,
        sugar=8.0,
        sodium=150.0,
        fiber=4.0,
        protein=10.0
    )

@pytest.fixture
def nutrition_factory():
    # Factory fixture to create Nutrition objects with customizable values for testing
    def _factory(recipe_id, calories=None,
        fat=None,
        saturated_fat=None,
        cholesterol=None,
        sodium=None,
        carbohydrates=None,
        fiber=None,
        sugar=None,
        protein=None
    ):
        return Nutrition(id=recipe_id, calories=calories,
            fat=fat,
            saturated_fat=saturated_fat,
            cholesterol=cholesterol,
            sodium=sodium,
            carbohydrates=carbohydrates,
            fiber=fiber,
            sugar=sugar,
            protein=protein)
    return _factory

@pytest.fixture
def full_recipe():
    return Nutrition(
        id=1,
        calories=300,
        fat=10.5,
        saturated_fat=3.2,
        cholesterol=50.0,
        sodium=200.0,
        carbohydrates=45.0,
        fiber=5.0,
        sugar=20.0,
        protein=15.0
    )