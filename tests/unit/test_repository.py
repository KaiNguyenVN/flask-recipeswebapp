from datetime import datetime
import tests.conftest
import pytest

from recipe.domainmodel.nutrition import Nutrition


# ----------------- Authentication -----------------

def test_add_and_get_user(repo, sample_user):
    repo.add_user(sample_user)
    assert repo.get_user("alice") is sample_user
    assert repo.get_user("bob") is None


# ----------------- Reviews -----------------

def test_add_review(repo, sample_user, sample_recipe, sample_review):
    repo.add_user(sample_user)
    repo.add_recipe(sample_recipe)

    repo.add_review(sample_review)

    # user and recipe should now have the review
    assert sample_review in sample_user.reviews
    assert sample_review in sample_recipe.reviews


"""
def test_remove_review(repo, sample_user, sample_recipe, sample_review):
    repo.add_user(sample_user)
    repo.add_recipe(sample_recipe)
    repo.add_review(sample_review)

    repo.remove_review(sample_review)

    assert sample_review not in sample_user.reviews
    assert sample_review not in sample_recipe.reviews
"""

# ----------------- Favourites -----------------

def test_add_and_remove_favourite(repo, sample_user, sample_recipe, sample_favourite):
    repo.add_user(sample_user)
    repo.add_recipe(sample_recipe)

    repo.add_favorite_recipe(sample_favourite)
    assert sample_favourite in sample_user.get_favourite_recipes

    repo.remove_favorite_recipe(sample_favourite)
    assert sample_favourite not in sample_user.get_favourite_recipes


# ----------------- Recipes -----------------

def test_add_and_get_recipe(repo, sample_recipe):
    repo.add_recipe(sample_recipe)
    recipes1 = repo.get_all_recipes()
    assert sample_recipe in recipes1


def test_get_recipe_by_id(repo, sample_recipe):
    repo.add_recipe(sample_recipe)
    assert repo.get_recipe_by_id(38) == sample_recipe
    assert repo.get_recipe_by_id(99) is None


# ----------------- Categories -----------------

def test_get_categories(repo, sample_category):
    repo._MemoryRepository__categories = {1: sample_category}
    categories = repo.get_categories()
    assert categories[1] == sample_category


# ----------------- Authors -----------------

def test_get_authors(repo, sample_author):
    repo._MemoryRepository__authors = {1: sample_author}
    authors = repo.get_authors()
    assert authors[1] == sample_author


# ----------------- Nutrition -----------------

def test_get_nutrition_by_recipe_id(repo):
    n = Nutrition(1, 100, 10, 20, 30)  # id, calories, fat, protein, carbs
    repo._MemoryRepository__nutrition = {1: n}
    result = repo.get_nutrition_by_recipe_id(1)
    assert result == n
    assert repo.get_nutrition_by_recipe_id(99) is None