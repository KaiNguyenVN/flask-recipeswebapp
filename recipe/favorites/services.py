from recipe.adapters.repository import AbstractRepository


class ReviewException(Exception):
    pass


class FavouriteException(Exception):
    pass

def get_favourite_recipes(username, repo: AbstractRepository):
    user = repo.get_user(username)
    return [f.recipe for f in user.get_favourite_recipes]