from datetime import datetime
from typing import List

from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.domainmodel.author import Author
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User
from recipe.domainmodel.review import Review

"""----------------------- Recipe -------------------"""

def test_repository_can_get_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    recipes = repo.get_all_recipes()
    assert len(recipes) == 13

def test_repository_can_add_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    authors = repo.get_authors()
    categories = repo.get_categories()

    if authors and categories:
        author = authors[0]
        category = categories[0]

        recipe1 = Recipe(5001, 'Test recipe 1', author, 30, 15,
                        datetime(2023, 1, 1), 'Test description', [], category,
                        ['1 cup'], ['flour'], 4.5, None, '4', '1 batch', ['Mix ingredients'])
        recipe2 = Recipe(5002, 'Test recipes 2', author, 45, 20,
                        datetime(2023, 1, 2), 'Test description 2', [], category,
                        ['2 cups'], ['sugar'], 4.0, None, '6', '1 batch', ['Mix and bake'])

        repo.add_recipe(recipe1)
        repo.add_recipe(recipe2)

        assert repo.get_recipe_by_id(5001) == recipe1
        assert repo.get_recipe_by_id(5002) == recipe2

def test_repository_does_not_retrieve_a_non_existent_recipe(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    recipe = repo.get_recipe_by_id(9201901)  # Non-existing recipe id
    assert recipe is None

def test_repository_can_retrieve_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipes: List[Recipe] = repo.get_recipes(1, 4, 'name')

    assert len(recipes) == 4

    recipe_one = [recipe for recipe in recipes if recipe.name == 'Low-Fat Berry Blue Frozen Dessert'][0]
    recipe_two = [recipe for recipe in recipes if recipe.name == 'Best Lemonade'][0]
    recipe_three = [recipe for recipe in recipes if recipe.name == "Carina's Tofu-Vegetable Kebabs"][0]
    recipe_four = [recipe for recipe in recipes if recipe.name == 'Cabbage Soup'][0]

    assert recipe_one.author.name == 'Dancer'
    assert recipe_two.author.name == 'Stephen Little'
    assert recipe_three.author.name == 'Cyclopz'
    assert recipe_four.author.name == 'Duckie067'

def test_repository_can_retrieve_recipes_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    num_of_recipes = repo.get_number_of_recipes()

    assert num_of_recipes == 13

def test_repository_can_retrieve_all_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    num_of_recipes = repo.get_number_of_recipes()
    assert len(repo.get_recipes(1, 10, 'name')) == 10


"""----------------------- Authors -------------------"""
def test_repository_can_add_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(1, 'TurtleMe')
    repo.add_author(1, author)

    authors = repo.get_authors()
    assert any(a.id == author.id and a.name == author.name for a in authors)

def test_repository_can_retrieve_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    authors: List[Author] = repo.get_authors()

    assert len(authors) == 11

    author_one = [author for author in authors if author.name == 'Dancer'][0]
    author_two = [author for author in authors if author.name == 'Stephen Little'][0]
    author_three = [author for author in authors if author.name == 'Cyclopz'][0]
    author_four = [author for author in authors if author.name == 'Duckie067'][0]

    assert author_one.id == 1533
    assert author_two.id == 1566
    assert author_three.id == 1586
    assert author_four.id == 1538


"""----------------------- Category -------------------"""


"""----------------------- User -------------------"""


"""----------------------- Reviews -------------------"""


"""----------------------- Search recipes -------------------"""

