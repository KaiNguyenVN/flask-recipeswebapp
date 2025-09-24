from typing import List
from pathlib import Path
from recipe.adapters.repository import AbstractRepository
from recipe.adapters.datareader.csvreader import CSVReader
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User
from recipe.domainmodel.review import Review


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__recipes = []  # list of recipes
        self.__categories = {} #Dictionary to store categories by their id
        self.__nutrition = {}
        self.__authors = {}

        self.__users = {}  # Dictionary to store users by their usernames
        self.__reviews = []

    def retrieve_csv_data(self, data_path: Path):
        csv_reader = CSVReader(data_path)
        csv_reader.extract_data()
        self.__recipes = csv_reader.get_recipes()
        self.__categories = csv_reader.get_categories()
        self.__nutrition = csv_reader.get_nutrition()
        self.__authors = csv_reader.get_authors()

    """-----------------------Authentication actions-------------------"""

    def add_user(self, user: User):
        """ Adds a new user to the repository """
        self.__users[user.username] = user

    def get_user(self, user_name: str) -> any:
        """ Fetches a user by their username. """
        if user_name in self.__users:
            return self.__users[user_name]
        else:
            return None

    """-----------------------User actions-------------------"""

    def add_review(self, review: Review):
        """ Adds a review for a recipe. """
        user = self.get_user(review.username)
        user.add_review(review)
        recipe = self.get_recipe_by_id(review.recipe_id)
        recipe.add_review(review)
        self.__reviews.append(review)

    def remove_review(self, review: Review):
        user = self.get_user(review.username)
        if review in user.reviews:
            user.remove_review(review)

        recipe = self.get_recipe_by_id(review.recipe_id)
        if review in recipe.reviews:
            recipe.reviews.remove(review)

        if review in self.__reviews:
            self.__reviews.remove(review)


    def add_favorite_recipe(self, favorite: Favourite):
        """ Adds a recipe to a user's favorites list. """
        user = self.get_user(favorite.username)
        user.add_favourite_recipe(favorite)

    def remove_favorite_recipe(self, favorite: Favourite):
        """ Removes a recipe from a user's favorites list. """
        user = self.get_user(favorite.username)
        user.remove_favourite_recipe(favorite)

    def get_user_favorites(self, user_name: str) -> List[Favourite]:
        """ Returns a list of a user's favorite recipes. """
        user = self.get_user(user_name)
        return user.get_favourite_recipes


    """----------------------Recipe actions----------------------"""
    def get_recipes(self) -> List[Recipe]:
        return self.__recipes
    def get_categories(self) -> dict[int, Category]:
        return self.__categories
    def get_authors(self) -> dict[int, Author]:
        return self.__authors
    def add_recipe(self, recipe: Recipe) -> None:
        self.__recipes.append(recipe)
    def get_recipe_by_id(self, recipe_id: int):
        for recipe in self.__recipes:
            if recipe.id == recipe_id:
                return recipe
        else:
            return None
    def get_nutrition_by_recipe_id(self, recipe_id: int) -> Nutrition | None:
        for n in self.__nutrition:
            if n.id == recipe_id:
                return n
        return None


#data_path = Path('recipe/adapters/data/recipes.csv')
