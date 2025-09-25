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
    return Recipe(1, "Pizza", Author(1, "Chef John"))


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
    return Nutrition(1, 100, 10, 20, 30)

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
    repo.retrieve_csv_data(TEST_DATA_PATH)
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
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)