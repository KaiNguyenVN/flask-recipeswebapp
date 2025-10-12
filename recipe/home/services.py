from recipe.adapters.repository import AbstractRepository


def get_recipes(page: int, page_size: int, sort_method: str, repo: AbstractRepository):
    return repo.get_recipes(page, page_size, sort_method)

def get_categories(repo: AbstractRepository):
    return repo.get_categories()

def get_nutrition_by_recipe_id(recipe_id: int, repo: AbstractRepository):
    return repo.get_nutrition_by_recipe_id(recipe_id)