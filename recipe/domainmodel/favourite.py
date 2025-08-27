from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .recipe import Recipe
    from .user import User


class Favourite:
<<<<<<< HEAD
    # Hazziq - recipe = "Recipe"
=======
>>>>>>> 42aae8f1a9d2f47bdf83a05ef9abfd680762a8d3
    def __init__(self, favourite_id: int, user: User, recipe: "Recipe") -> None:
        if not isinstance(favourite_id, int) or favourite_id <= 0:
            raise ValueError("id must be a positive int.")
        self.__favourite_id = favourite_id
        self.__user = user
        self.__recipe = recipe

    @property
    def id(self) -> int:
        return self.__favourite_id
    @property
    def user(self) -> User:
        return self.__user
    @property
    def recipe(self) -> Recipe:
        return self.__recipe