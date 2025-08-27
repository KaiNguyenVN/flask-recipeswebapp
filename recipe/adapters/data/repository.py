from typing import List

from recipe import Author
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
    def get_nutrition(self) -> List[Nutrition]:
        pass