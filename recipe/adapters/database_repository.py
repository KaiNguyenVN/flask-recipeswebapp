from datetime import date
from pathlib import Path
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    """-----------------------User actions-------------------"""
    def add_user(self, user:User):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(User).filter(
                    User._User__username == user.username
                )
                if user not in query.all():
                    scm.session.add(user)
                    scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            query = self._session_cm.session.query(User).filter(
                User._User__username == user_name
            )
            user = query.one()
            # Populate the related data for consistent domain model interface
            self._populate_user_data(user)
        except NoResultFound:
            print(f'User {user_name} was not found')
        return user


    def add_review(self, review: Review):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(Review).filter(
                    Review._Review__id == review.review_id
                )
                if review not in query.all():
                    scm.session.add(review)
                    scm.commit()

    def remove_review(self, review: Review):
        pass

    def add_favorite_recipe(self, favorite: Favourite):
        pass

    def remove_favorite_recipe(self, favorite: Favourite):
        pass

    def get_user_favorites(self, user_name: str) -> List[Favourite]:
        pass

    """----------------------Recipe actions----------------------"""
    def get_recipes(self) -> List[Recipe]:
        pass

    def get_authors(self) -> dict[int, Author]:
        pass

    def get_categories(self) -> dict[str, Category]:
        pass

    def add_recipe(self, recipe: Recipe) -> None:
        pass

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        pass

    def get_nutrition_by_recipe_id(self, recipe_id: int) -> Nutrition:
        pass

    def get_recipes_sorted_by_nutrition(self, descending: bool = True) -> List[Recipe]:
        pass

    def get_healthy_recipes(self, min_rating: float = 3.5) -> List[Recipe]:
        pass

    """-----------------------population-------------------"""
    def add_category(self, id: str,category: Category) -> None:
        pass

    def add_nutrition(self, id: str, nutri: Nutrition) -> None:
        pass

    def add_author(self, id:int, author: Author) -> None:
        pass

    def add_instruction(self, instruction: RecipeInstruction) -> None:
        pass

    def add_image(self, image: RecipeImage) -> None:
        pass

    def add_ingredient(self, ingredient: RecipeIngredient) -> None:
        pass