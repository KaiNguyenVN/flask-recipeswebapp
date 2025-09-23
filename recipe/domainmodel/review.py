from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recipe.domainmodel.user import User
    from recipe.domainmodel.recipe import Recipe


class Review:
    # Hazziq - recipe: "Recipe" to fix error
    def __init__(self, review_id: int, user: "User", recipe: "Recipe", rate: int, review: str, date: datetime = None) -> None:
        if not isinstance(review_id, int) or review_id <= 0:
            raise ValueError("id must be a positive int.")
        if not isinstance(rate, int) or rate <= 0:
            raise ValueError("rate must be a positive int.")

        self.__review_id = review_id
        self.__user = user
        self.__recipe = recipe
        self.__rate = rate
        self.__review = review
        self.__date = date if date else datetime.now()

    def __repr__(self) -> str:
        return f"Review(id={self.__review_id}, user={self.user}, rate={self.rate}, review={self.review}, date={self.date})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            raise TypeError("Comparison must be between Review instances")
        else:
            return self.rate == other.rate
    def __lt__(self, other) -> bool:
        if not isinstance(other, Review):
            raise TypeError("Comparison must be between Review instances")
        else:
            return self.rate < other.rate
    def __hash__(self) -> int:
        return hash(self.__review_id)

    @property
    def review_id(self) -> int:
        return self.__review_id
    @property
    def user(self) -> 'User':
        return self.__user
    @property
    def recipe(self) -> 'Recipe':
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