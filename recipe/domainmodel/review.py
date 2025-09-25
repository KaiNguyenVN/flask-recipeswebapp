from datetime import datetime

class Review:
    # Hazziq - recipe: "Recipe" to fix error
    def __init__(self, username:str, recipe_id:int, rating: int, review: str, date: datetime, review_id = None) -> None:
        if not isinstance(rating, int) or rating <= 0 or rating > 5:
            raise ValueError("rating must be a positive value and less than 5.")
        if review_id is not None:
            if not isinstance(review_id, int) or review_id <= 0:
                raise ValueError("review_id must be a positive value.")

        self.__review_id = review_id
        self.__username = username
        self.__recipe_id = recipe_id
        self.__rating = rating
        self.__review = review
        self.__date = date if date else datetime.now()

    def __repr__(self) -> str:
        return f"Review(id={self.__review_id}, user={self.__username}, rate={self.rating}, review={self.review}, date={self.date})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            raise TypeError("Comparison must be between Review instances")
        else:
            return self.rating == other.rating
    def __lt__(self, other) -> bool:
        if not isinstance(other, Review):
            raise TypeError("Comparison must be between Review instances")
        else:
            return self.rating < other.rating
    def __hash__(self) -> int:
        return hash(self.__review_id)

    @property
    def review_id(self) -> int:
        return self.__review_id
    @property
    def username(self) -> str:
        return self.__username
    @property
    def recipe_id(self) -> int:
        return self.__recipe_id
    @property
    def rating(self) -> int:
        return self.__rating
    @property
    def review(self) -> str:
        return self.__review
    @property
    def date(self) -> datetime:
        return self.__date