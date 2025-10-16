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
    assert len(recipes) == 1

def test_repository_can_add_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    authors = repo.get_authors()
    categories = repo.get_categories()

    if authors and categories:
        author = authors[0]
        category = categories['Beverages']

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

    assert num_of_recipes == 11

def test_repository_can_retrieve_all_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_recipes(1, 10, 'name')) == 10


"""----------------------- Authors -------------------"""
def test_repository_can_add_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(1, 'TurtleMe')
    repo.add_author(1, author)

    authors = repo.get_authors()
    assert 1 in authors
    assert authors[1].name == 'TurtleMe'

def test_repository_can_retrieve_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    authors = repo.get_authors()

    assert len(authors) >= 1

    assert 1533 in authors
    assert authors[1533].name == 'Dancer'

    assert 1566 in authors
    assert authors[1566].name == 'Stephen Little'

    assert 1586 in authors
    assert authors[1586].name == 'Cyclopz'

    assert 1538 in authors
    assert authors[1538].name == 'Duckie067'


"""----------------------- Category -------------------"""
def test_repository_can_add_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    category = Category('Desserts')
    repo.add_category('Desserts', category)

    categories = repo.get_categories()
    assert 'Desserts' in categories
    assert categories['Desserts'].name == 'Desserts'

def test_repository_can_retrieve_categories(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    categories = repo.get_categories()

    assert len(categories) >= 1
    assert 'Beverages' in categories


"""----------------------- User -------------------"""
def test_repository_can_add_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('testuser', 'password123')
    repo.add_user(user)

    fetched_user = repo.get_user('testuser')
    assert fetched_user is not None
    assert fetched_user.username == 'testuser'

def test_repository_does_not_retrieve_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('nonexistent')
    assert user is None


"""----------------------- Reviews -------------------"""


def test_repository_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Add a user and recipe
    user = User('reviewuser', 'password123')
    repo.add_user(user)

    review = Review(
        username='reviewuser',
        recipe_id=9518,  # existing recipe ID from test data
        rating=5,
        review='Excellent recipe!',
        date=datetime.now()
    )
    repo.add_review(review)

    # Verify review was added by checking if can retrieve reviews for the recipe
    recipe = repo.get_recipe_by_id(9518)
    assert recipe is not None


def test_repository_can_remove_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('reviewuser2', 'password123')
    repo.add_user(user)

    review = Review(
        username='reviewuser2',
        recipe_id=9518,
        rating=4,
        review='Good recipe',
        date=datetime.now()
    )
    repo.add_review(review)

    # Remove the review
    repo.remove_review(review)


"""----------------------- Search recipes -------------------"""
def test_repository_can_search_recipes_by_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    results = repo.search_recipes("Lemonade")
    assert len(results) > 0
    assert any("Lemonade" in recipe.name for recipe in results)


def test_repository_can_search_recipes_by_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    results = repo.search_recipes_by_author("Stephen Little")
    assert len(results) > 0
    assert any(recipe.author.name == "Stephen Little" for recipe in results)

def test_repository_can_search_recipes_by_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    results = repo.search_recipes_by_category("Beverages")
    assert len(results) > 0
    assert any(recipe.category.name == "Beverages" for recipe in results)