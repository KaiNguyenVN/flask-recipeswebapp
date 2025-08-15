from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.user import User


class Favourite:
# TODO: Complete the implementation of the Favourite class.
    def __init__(self, id: int, user: User, recipe: Recipe) -> None:
        if not isinstance(id, int) or id <= 0:
            raise ValueError("id must be a positive int.")
        self.__id = id
        self.__user = user
        self.__recipe = recipe

    @property
    def id(self) -> int:
        return self.__id
    @property
    def user(self) -> User:
        return self.__user
    @property
    def recipe(self) -> Recipe:
        return self.__recipe
