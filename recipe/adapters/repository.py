from typing import List
from pathlib import Path
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
#from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
import abc

from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

repo_instance = None

class AbstractRepository(abc.ABC):

    """-----------------------Authentication-------------------"""
    @abc.abstractmethod
    def add_user(self, user: User):
        # Adds an user to repo
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str) -> User:
        # returns username from repo. If such username doesn't exist
        raise NotImplementedError

    """-----------------------User actions-------------------"""
    @abc.abstractmethod
    def add_review(self, review: Review):
        raise NotImplementedError

    def remove_review(self, review: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def add_favorite_recipe(self, favorite: Favourite):
        """ Adds a recipe to the user's favorites list. """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favorite_recipe(self, favorite: Favourite):
        """ Removes a recipe from the user's favorites list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_favorites(self, user_name: str) -> List[Favourite]:
        """ Returns a list of recipes in the user's favorites. """
        raise NotImplementedError

    """----------------------Recipe actions----------------------"""
    @abc.abstractmethod
    def get_recipes(self) -> List[Recipe]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self) -> dict[int, Author]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_categories(self) -> dict[str, Category]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        raise NotImplementedError

    @abc.abstractmethod
    def get_nutrition_by_recipe_id(self, recipe_id: int) -> Nutrition:
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_sorted_by_nutrition(self, descending: bool = True) -> List[Recipe]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_healthy_recipes(self, min_rating: float = 3.5) -> List[Recipe]:
        raise NotImplementedError

    """-----------------------population-------------------"""

    @abc.abstractmethod
    def add_category(self, id: str,category: Category) -> None:
        raise NotImplementedError
    @abc.abstractmethod
    def add_nutrition(self, id:int, nutri: Nutrition) -> None:
        raise NotImplementedError
    @abc.abstractmethod
    def add_author(self, id:int, author: Author) -> None:
        raise NotImplementedError

