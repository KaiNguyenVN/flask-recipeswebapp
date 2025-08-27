from typing import List
from pathlib import Path
from recipe.adapters.repository import AbstractRepository
from recipe.adapters.datareader.csvreader import CSVReader
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition


class MemoryRepository(AbstractRepository):
    def __init__(self, path: Path):
        reader = CSVReader(path)
        reader.extract_data()
        self.__recipes = reader.get_recipes()
        self.__categories = reader.get_categories()
        self.__nutrition = reader.get_nutrition()
        self.__authors = reader.get_authors()
    def get_recipes(self) -> List[Recipe]:
        return self.__recipes
    def get_categories(self) -> List[Category]:
        return self.__categories
    def get_nutrition(self) -> List[Nutrition]:
        return self.__nutrition
    def get_authors(self) -> List[Author]:
        return self.__authors
    def add_recipe(self, recipe: Recipe) -> None:
        self.__recipes.append(recipe)

data_path = Path('recipe/adapters/data/recipes.csv')
repo_instance = MemoryRepository(data_path)