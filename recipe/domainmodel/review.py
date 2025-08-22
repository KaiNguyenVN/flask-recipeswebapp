from __future__ import annotations # Hazziq - fix error
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .recipe import Recipe

class Review:
# TODO: Complete the implementation of the Review class.
    # Hazziq - recipe: "Recipe" to fix error
    def __init__(self, id: int, user: "User", recipe: "Recipe", rate: int, review: str, date: datetime = None) -> None:
        if not isinstance(id, int) or id <= 0:
            raise ValueError("id must be a positive int.")
        if not isinstance(rate, int) or rate <= 0:
            raise ValueError("rate must be a positive int.")

        self.__id = id
        self.__user = user
        self.__recipe = recipe
        self.__rate = rate
        self.__review = review
        self.__date = date if date else datetime.now()

    @property
    def id(self) -> int:
        return self.__id
    @property
    def user(self) -> User:
        return self.__user
    @property
    def recipe(self) -> Recipe:
        return self.__recipe
    @property
    def rate(self) -> int:
        return self.__rate
    @property
    def review(self) -> str:
        return self.__review
    @property
    def date(self) -> datetime:
        return self.__date

