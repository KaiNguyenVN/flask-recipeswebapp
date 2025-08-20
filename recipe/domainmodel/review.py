from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recipe.domainmodel.user import User


class Review:
# TODO: Complete the implementation of the Review class.
    def __init__(self, id: int, user: "User", rate: int, review: str, date: datetime = None) -> None:
        if not isinstance(id, int) or id <= 0:
            raise ValueError("id must be a positive int.")
        if not isinstance(rate, int) or rate <= 0:
            raise ValueError("rate must be a positive int.")

        self.__id = id
        self.__user = user
        self.__rate = rate
        self.__review = review
        self.__date = date if date else datetime.now()

    def __repr__(self) -> str:
        return f"Review(id={self.id}, user={self.user}, rate={self.rate}, review={self.review}, date={self.date})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        else:
            return self.rate == other.rate
    def __lt__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        else:
            return self.rate < other.rate
    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def id(self) -> int:
        return self.__id
    @property
    def user(self) -> "User":
        return self.__user
    @property
    def rate(self) -> int:
        return self.__rate
    @property
    def review(self) -> str:
        return self.__review
    @property
    def date(self) -> datetime:
        return self.__date

