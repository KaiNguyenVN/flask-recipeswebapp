from abc import abstractproperty
from typing import List
import os
from recipe.adapters.data.repository import AbstractRepository
from recipe.adapters.datareader.csvreader import CSVReader
from recipe import Recipe, Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "recipes.csv")
reader = CSVReader(csv_path)
reader.extract_data()

recipes = reader.get_recipes()
categories = reader.get_categories()
nutrition = reader.get_nutrition()
authors = reader.get_authors()

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__recipes = recipes
        self.__categories = categories
        self.__nutrition = nutrition
        self.__authors = authors
    def get_recipes(self) -> List[Recipe]:
        return self.__recipes
    def get_categories(self) -> List[Category]:
        return self.__categories
    def get_nutrition(self) -> List[Nutrition]:
        return self.__nutrition
    def get_authors(self) -> List[Author]:
        return self.__authors