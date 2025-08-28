from typing import List
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_recipes(self) -> List[Recipe]:
        pass
    @abc.abstractmethod
    def get_authors(self) -> List[Author]:
        pass
    @abc.abstractmethod
    def get_categories(self) -> List[Category]:
        pass
    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe) -> None:
        pass
    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        pass