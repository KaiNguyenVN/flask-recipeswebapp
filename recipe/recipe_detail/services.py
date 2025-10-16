from datetime import datetime

from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite
from recipe.adapters.repository import AbstractRepository


class ReviewException(Exception):
    pass


class FavouriteException(Exception):
    pass

def add_review(username: str, recipe_id: int, review_text: str, rating: int, date: datetime, repo: AbstractRepository):
    """Add a review + rating to a recipe."""
    recipe = repo.get_recipe_by_id(recipe_id)
    user = repo.get_user(username)

    if recipe is None or user is None:
        raise ReviewException("Recipe or user not found")

    # Create review object
    review = Review(username = username, recipe = recipe, rating=rating, review=review_text, date=date)
    # Store review in repo
    repo.add_review(review)
    return review

def remove_review(username: str, recipe_id: int, review_id: int, repo: AbstractRepository):
    """Remove a review if it belongs to the given user."""
    recipe = repo.get_recipe_by_id(recipe_id)
    if recipe is None:
        raise ReviewException("Recipe not found")

    review_to_remove = next((r for r in recipe.reviews if r.review_id == review_id and r.username == username), None)
    if review_to_remove is None:
        raise ReviewException("Review not found or not owned by user")

    repo.remove_review(review_to_remove)
    return review_to_remove


def get_reviews_for_recipe(recipe_id: int, repo: AbstractRepository):
    """Return all reviews for a recipe."""
    recipe = repo.get_recipe_by_id(recipe_id)
    return recipe.reviews

def add_favorite_recipe(username: str, recipe_id: int, repo: AbstractRepository):
    """Add a recipe to user's favourites."""
    user = repo.get_user(username)
    recipe = repo.get_recipe_by_id(recipe_id)

    if not user or not recipe:
        raise FavouriteException("User or recipe not found")

    fav = Favourite(username=username, recipe=recipe, favourite_id=recipe_id)
    repo.add_favorite_recipe(fav)
    return fav


def remove_favorite_recipe(username: str, recipe_id: int, repo: AbstractRepository):
    """Remove a recipe from user's favourites."""
    user = repo.get_user(username)
    recipe = repo.get_recipe_by_id(recipe_id)

    if not user or not recipe:
        raise FavouriteException("User or recipe not found")
    fav = Favourite(username=username, recipe=recipe, favourite_id=recipe_id)
    repo.remove_favorite_recipe(fav)

def is_favorited(username, recipe_id, repo):
    """
    Returns True if the given recipe is already in the user's favorites.
    """
    favorites = repo.get_user_favorites(username)
    return any(f.id == recipe_id for f in favorites)