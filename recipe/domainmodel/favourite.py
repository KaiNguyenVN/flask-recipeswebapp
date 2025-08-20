from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recipe.domainmodel.user import User
    from recipe.domainmodel.recipe import Recipe

class Favourite:
# TODO: Complete the implementation of the Favourite class.
    def __init__(self, id: int, user: "User", recipe: "Recipe") -> None:
        if not isinstance(id, int) or id <= 0:
            raise ValueError("id must be a positive int.")
        self.__id = id
        self.__user = user
        self.__recipe = recipe

    def __repr__(self) -> str:
        return f"Favorite_recipe(id={self.id}, user={self.user.username}, recipe={self.recipe.name})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Favourite):
            return False
        else:
            return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Favourite):
            return False
        else:
            return self.id < other.id

    @property
    def id(self) -> int:
        return self.__id
    @property
    def user(self) -> "User":
        return self.__user
    @property
    def recipe(self) -> "Recipe":
        return self.__recipe
