# Hazziq add both from import and add if type checking
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .recipe import Recipe

class Favourite:
    # Hazziq - recipe = "Recipe"
    def __init__(self, favourite_id: int, username: str, recipe: "Recipe") -> None:
        if not isinstance(favourite_id, int) or favourite_id <= 0:
            raise ValueError("id must be a positive int.")
        self.__favourite_id = favourite_id
        self.__username = username
        self.__recipe = recipe

    def __repr__(self) -> str:
        return f"Favorite_recipe(id={self.__favourite_id}, username={self.__username}, recipe={self.recipe.name})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Favourite):
            raise TypeError("Comparison must be between Favorite instances")
        else:
            return self.__favourite_id == other.__favourite_id

    def __hash__(self) -> int:
        return hash(self.__favourite_id)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Favourite):
            raise TypeError("Comparison must be between Favorite instances")
        else:
            return self.__favourite_id < other.__favourite_id

    @property
    def id(self) -> int:
        return self.__favourite_id
    @property
    def username(self) -> str:
        return self.__username
    @property
    def recipe(self) -> Recipe:
        return self.__recipe
