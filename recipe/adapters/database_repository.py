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
                    scm.session.merge(review)
                    scm.commit()

    def remove_review(self, review: Review):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(Review).filter(
                    Review._Review__id == review.review_id
                )
                if review in query.all():
                    scm.session.delete(review)
                    scm.commit()


    def add_favorite_recipe(self, favourite: Favourite):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(Favourite).filter(
                    Favourite._Favourite__id == favourite.id
                )
                if favourite not in query.all():
                    scm.session.merge(favourite)
                    scm.commit()

    def remove_favorite_recipe(self, favourite: Favourite):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(Favourite).filter(
                    Favourite._Favourite__id == favourite.id
                )
                if favourite in query.all():
                    scm.session.delete(favourite)
                    scm.commit()

    def get_user_favorites(self, user_name: str) -> List[Favourite]:
        favourites = None
        try:
            query = self._session_cm.session.query(Favourite).filter(
                Favourite._Favourite__username == user_name
            )
            favourites = query.all()
            # Populate the related data for consistent domain model interface
        except NoResultFound:
            print(f'{user_name} Favourites was not found')
        return favourites

    """----------------------Recipe actions----------------------"""
    def get_all_recipes(self) -> List[Recipe]:
        with self._session_cm as scm:
            recipes: list[Recipe] = scm.session.query(Recipe).all()
            for recipe in recipes:
                self._populate_recipe_data_in_session(recipe, scm.session)
            return recipes

    def get_recipes(self, page: int, page_size: int, sort_method: str) -> List[Recipe]:
        # Sanitize pagination inputs
        if page is None or page < 1:
            page = 1
        if page_size is None or page_size < 1:
            page_size = 10
        offset = (page - 1) * page_size

        with self._session_cm as scm:
            q = scm.session.query(Recipe)

            # Basic sort options supported by current schema
            sort_method = (sort_method or 'name').lower()
            if sort_method in ('name', 'name_asc'):
                q = q.order_by(Recipe._Recipe__name.asc(), Recipe._Recipe__id.asc())
            elif sort_method in ('name_desc', 'desc_name'):
                q = q.order_by(Recipe._Recipe__name.desc(), Recipe._Recipe__id.asc())
            elif sort_method in ('id', 'id_asc'):
                q = q.order_by(Recipe._Recipe__id.asc())
            elif sort_method in ('id_desc', 'desc_id'):
                q = q.order_by(Recipe._Recipe__id.desc())
            else:
                # Fallback to name ascending if unknown
                q = q.order_by(Recipe._Recipe__name.asc(), Recipe._Recipe__id.asc())

            recipes: List[Recipe] = q.offset(offset).limit(page_size).all()

            # Populate related data (images, ingredients, instructions, etc.)
            for r in recipes:
                self._populate_recipe_data_in_session(r, scm.session)

            return recipes

    def get_authors(self) -> dict[int, Author]:
        query = self._session_cm.session.query(Author)
        authors: list[Author] = query.all()
        dic = {i.id: i for i in authors}
        # Populate the related data for consistent domain model interface
        return dic

    def get_categories(self) -> dict[str, Category]:
        query = self._session_cm.session.query(Category)
        categories: list[Category] = query.all()
        dic = {i.name: i for i in categories}
        # Populate the related data for consistent domain model interface
        return dic

    def add_recipe(self, recipe: Recipe) -> None:
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(Recipe).filter(
                    Recipe._Recipe__id == recipe.id
                )
                if recipe not in query.all():
                    scm.session.merge(recipe)
                    scm.commit()

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        recipe = None
        try:
            query = self._session_cm.session.query(Recipe).filter(
                Recipe._Recipe__id == recipe_id
            )
            recipe = query.one()
            # Populate the related data for consistent domain model interface
            self._populate_recipe_data(recipe)
        except NoResultFound:
            print(f'Recipe {recipe_id} was not found')
        return recipe

    def get_nutrition_by_recipe_id(self, recipe_id: int) -> Nutrition:
        query = self._session_cm.session.query(Nutrition).filter(
            Nutrition._Nutrition__id == recipe_id
        )
        nutri = query.one()
        return nutri




    """-----------------------population-------------------"""
    def add_category(self, id: str,category: Category) -> None:
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(Category).filter(
                    Category._Category__id == category.id
                )
                if category not in query.all():
                    scm.session.add(category)
                    scm.commit()

    def add_nutrition(self, id: str, nutri: Nutrition) -> None:
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(Nutrition).filter(
                    Nutrition._Nutrition__id == nutri.id
                )
                if nutri not in query.all():
                    scm.session.add(nutri)
                    scm.commit()

    def add_author(self, id:int, author: Author) -> None:
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(Author).filter(
                    Author._Author__id == author.id
                )
                if author not in query.all():
                    scm.session.add(author)
                    scm.commit()

    def add_instruction(self, instruction: RecipeInstruction) -> None:
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(RecipeInstruction).filter(
                    RecipeInstruction._RecipeInstruction__id == instruction.id
                )
                if instruction not in query.all():
                    scm.session.add(instruction)
                    scm.commit()

    def add_image(self, image: RecipeImage) -> None:
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(RecipeImage).filter(
                    RecipeImage._RecipeImage__id == image.id
                )
                if image not in query.all():
                    scm.session.add(image)
                    scm.commit()

    def add_ingredient(self, ingredient: RecipeIngredient) -> None:
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                query = scm.session.query(RecipeIngredient).filter(
                    RecipeIngredient._RecipeIngredient__id == ingredient.id
                )
                if ingredient not in query.all():
                    scm.session.add(ingredient)
                    scm.commit()

    def add_multiple_instruction(self, instruction: list[RecipeInstruction]) -> None:
        with self._session_cm as scm:
            for i in instruction:
                scm.session.add(i)
            scm.commit()

    def add_multiple_ingredient(self, ingredients: list[RecipeIngredient]) -> None:
        with self._session_cm as scm:
            for i in ingredients:
                scm.session.add(i)
            scm.commit()

    def add_multiple_category(self, category: dict[str, Category]) -> None:
        with self._session_cm as scm:
            for i in category:
                scm.session.merge(category[i])
            scm.commit()

    def add_multiple_nutrition(self, nutri: dict[int, Nutrition]) -> None:
        with self._session_cm as scm:
            for i in nutri:
                scm.session.merge(nutri[i])
            scm.commit()

    def add_multiple_author(self, author: dict[int, Author]) -> None:
        with self._session_cm as scm:
            for i in author:
                scm.session.merge(author[i])
            scm.commit()

    def add_multiple_image(self, image: list[RecipeImage]) -> None:
        with self._session_cm as scm:
            for i in image:
                scm.session.add(i)
            scm.commit()

    def add_multiple_recipe(self, recipes: List[Recipe]) -> None:
        with self._session_cm as scm:
            for i in recipes:
                scm.session.merge(i)
            scm.commit()


    """-----------------------populate data-------------------"""
    def _populate_recipe_data(self, recipe: Recipe) -> None:
        if recipe is None:
            return

            # Use the same session context
        with self._session_cm as scm:
            self._populate_recipe_data_in_session(recipe, scm.session)

    def _populate_recipe_data_in_session(self, recipe: Recipe, session):
        if recipe is None:
            return

        # Load and populate images
        recipe_images = session.query(RecipeImage).filter(
            RecipeImage._RecipeImage__recipe_id == recipe.id
        ).order_by(RecipeImage._RecipeImage__position).all()

        if recipe_images:
            image_urls = [img.url for img in recipe_images]
            recipe._Recipe__images = image_urls
        else:
            print(f"DEBUG: No images found for recipe {recipe.id}")

        # Load and populate ingredient
        recipe_ingredients = session.query(RecipeIngredient).filter(
            RecipeIngredient._RecipeIngredient__recipe_id == recipe.id
        ).order_by(RecipeIngredient._RecipeIngredient__position).all()

        if recipe_ingredients:
            recipe._Recipe__ingredients = [i.ingredient for i in recipe_ingredients]
            recipe._Recipe__ingredient_quantities = [i.quantity for i in recipe_ingredients]

        # Load and populate instruction
        recipe_instructions = session.query(RecipeInstruction).filter(
            RecipeInstruction._RecipeInstruction__recipe_id == recipe.id
        ).order_by(RecipeInstruction._RecipeInstruction__position).all()
        if recipe_instructions:
            recipe._Recipe__instructions = [i.step for i in recipe_instructions]

