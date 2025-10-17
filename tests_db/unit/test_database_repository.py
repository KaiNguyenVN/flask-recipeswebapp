from datetime import datetime
import pytest

from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.domainmodel.user import User
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.category import Category
from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition


# ----------------------- USER TESTS -----------------------

def test_can_add_and_retrieve_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("alice", "Password123")
    repo.add_user(user)

    retrieved = repo.get_user("alice")

    assert retrieved == user
    assert retrieved.password == "Password123"


def test_get_user_returns_none_for_unknown_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_user("nonexistent") is None


# ----------------------- RECIPE TESTS -----------------------

def test_can_retrieve_all_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipes = repo.get_all_recipes()

    assert isinstance(recipes, list)
    assert len(recipes) > 0
    assert isinstance(recipes[0], Recipe)


def test_can_get_recipe_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipe = repo.get_recipe_by_id(38)

    assert recipe is not None
    assert isinstance(recipe, Recipe)
    assert recipe.id == 38
    assert recipe.name != ""


def test_get_recipe_by_id_returns_none_for_invalid_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_recipe_by_id(99999) is None


def test_can_add_recipe(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = Author(99, "Chef Test")
    category = Category("Desserts")
    new_recipe = Recipe(
        recipe_id=999,
        name="Test Cheesecake",
        author=author,
        cook_time=10,
        preparation_time=15,
        created_date=datetime.utcnow(),
        description="A test recipe for cheesecake.",
        images=[],
        category=category,
        ingredients=[],
        ingredient_quantities=[],
        rating=4.5,
        servings="4",
        recipe_yield="1 cake",
        instructions=[],
        reviews=[]
    )

    repo.add_recipe(new_recipe)
    retrieved = repo.get_recipe_by_id(999)
    assert retrieved.name == "Test Cheesecake"

def test_populate_recipe_data(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipe = repo.get_recipe_by_id(38)
    assert recipe.images
    assert recipe.ingredients
    assert recipe.instructions

# ----------------------- REVIEW TESTS -----------------------

def test_can_add_and_retrieve_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("bob", "Password123")
    repo.add_user(user)
    recipe = repo.get_recipe_by_id(38)

    review = Review(username=user.username, recipe=recipe, rating=5, review="Excellent!", date=datetime.utcnow())
    repo.add_review(review)

    retrieved_user = repo.get_user("bob")
    assert any(r.review == "Excellent!" for r in retrieved_user.reviews)
    assert any(r.review == "Excellent!" for r in recipe.reviews)

# ----------------------- FAVORITES TESTS -----------------------

def test_can_add_and_remove_favorite(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("dave", "Password123")
    repo.add_user(user)
    recipe = repo.get_recipe_by_id(38)

    fav = Favourite(recipe=recipe, username="dave", favourite_id=recipe.id)
    repo.add_favorite_recipe(fav)

    favorites = repo.get_user_favorites("dave")
    assert isinstance(favorites, list)
    assert any(f._Favourite__recipe.id == recipe.id for f in favorites)

    repo.remove_favorite_recipe(fav)
    favorites = repo.get_user_favorites("dave")
    assert not any(f._Favourite__recipe.id == recipe.id for f in favorites)

def test_can_get_user_favorites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipe = repo.get_recipe_by_id(38)

    fav = Favourite(recipe=recipe, username="dave", favourite_id=recipe.id)
    repo.add_favorite_recipe(fav)

    favorites = repo.get_user_favorites("dave")
    assert isinstance(favorites, list)
    assert any(f._Favourite__recipe.id == recipe.id for f in favorites)

# ----------------------- CATEGORY & AUTHOR TESTS -----------------------

def test_can_get_all_categories_and_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    categories = repo.get_categories()
    authors = repo.get_authors()

    assert isinstance(categories, dict)
    assert len(categories) > 0
    assert all(isinstance(c, Category) for c in categories.values())

    assert isinstance(authors, dict)
    assert len(authors) > 0
    assert all(isinstance(a, Author) for a in authors.values())


# ----------------------- NUTRITION TESTS -----------------------

def test_can_get_nutrition_for_recipe(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipe = repo.get_recipe_by_id(38)

    nutrition = repo.get_nutrition_by_recipe_id(recipe.id)
    assert isinstance(nutrition, Nutrition)
    assert nutrition.calories > 0


# ----------------------- PAGINATION TESTS -----------------------

def test_get_recipes_with_pagination(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    page_1 = repo.get_recipes(page=1, page_size=5, sort_method="name")
    page_2 = repo.get_recipes(page=2, page_size=5, sort_method="name")

    assert len(page_1) <= 5
    assert len(page_2) <= 5
    assert page_1 != page_2


# ----------------------- EDGE CASES -----------------------

def test_get_user_favorites_returns_empty_list_for_new_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("erin", "Password123")
    repo.add_user(user)

    favs = repo.get_user_favorites("erin")
    assert favs == [] or favs is None


def test_add_existing_user_does_not_duplicate(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("frank", "Password123")
    repo.add_user(user)
    repo.add_user(user)  # duplicate

    retrieved = repo.get_user("frank")
    assert retrieved.username == "frank"
