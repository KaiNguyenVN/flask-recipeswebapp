import pytest
from pathlib import Path

from recipe.domainmodel.user import User
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.adapters.memory_repository import MemoryRepository

@pytest.fixture
def repo():
    data_path = Path('tests/data/test_recipes.csv')
    repo = MemoryRepository(data_path)
    return repo

def test_get_recipes(repo):
    recipes = repo.get_recipes()
    assert len(recipes) == 3
    assert recipes[0].id == 38
    assert recipes[1].id == 40
    assert recipes[2].id == 41

def test_get_recipe_by_id(repo):
    recipe = repo.get_recipe_by_id(38)

    assert recipe.name == "Low-Fat Berry Blue Frozen Dessert"
    assert recipe.author.name == "Dancer"
    assert recipe.author.id == 1533

def test_add_recipe(repo):
    author = Author(1, "sid")
    recipe = Recipe(1, "coke", author)
    repo.add_recipe(recipe)
    assert repo.get_recipe_by_id(1) != None
    assert repo.get_recipe_by_id(1).name == "coke"
    assert repo.get_recipe_by_id(1).author == author

def test_get_categories(repo):
    categories = repo.get_categories()
    categories.sort(key=lambda x: x.name)
    assert len(categories) == 3
    assert categories[0].name == "Beverages"
    assert categories[1].name == "Frozen Desserts"
    assert categories[2].name == "Soy/Tofu"


def test_get_authors(repo):
    authors = repo.get_authors()
    authors.sort(key=lambda x: x.id)
    assert len(authors) == 3
    assert authors[0].id == 1533
    assert authors[1].id == 1566
    assert authors[2].id == 1586

