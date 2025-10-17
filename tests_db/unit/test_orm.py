import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from recipe.domainmodel.user import User
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition


# ---------------- USER TESTS ----------------

def test_add_and_retrieve_user(empty_session):
    user = User("Alice", "Password123")
    empty_session.add(user)
    empty_session.commit()

    row = empty_session.execute("SELECT username, password FROM user").fetchone()
    assert row == ("Alice", "Password123")

    retrieved = empty_session.query(User).one()
    assert retrieved.username == "Alice"
    assert retrieved.password == "Password123"


def test_username_unique_constraint(empty_session):
    user = User("Bob", "abc123")
    empty_session.add(user)
    empty_session.commit()
    empty_session.expunge_all()
    with pytest.raises(IntegrityError):
        duplicate = User("Bob", "def456")
        empty_session.add(duplicate)
        empty_session.commit()


# ---------------- AUTHOR & CATEGORY TESTS ----------------

def test_insert_author_and_category(empty_session):
    author = Author(1, "Gordon Ramsay")
    category = Category("Dinner", category_id=1)

    empty_session.add(author)
    empty_session.add(category)
    empty_session.commit()

    authors = [r[0] for r in empty_session.execute("SELECT name FROM authors")]
    categories = [r[0] for r in empty_session.execute("SELECT name FROM category")]

    assert authors == ["Gordon Ramsay"]
    assert categories == ["Dinner"]


# ---------------- RECIPE TESTS ----------------

def test_insert_recipe_with_author_and_category(empty_session):
    author = Author(2, "Jamie Oliver")
    category = Category("Lunch", category_id=2)
    recipe = Recipe(
        recipe_id=1,
        name="Grilled Cheese",
        author=author,
        cook_time=10,
        preparation_time=5,
        created_date=datetime.utcnow(),
        description="Simple sandwich",
        category=category,
        rating=4.5,
        servings="1",
        recipe_yield="1 sandwich",
    )

    empty_session.add(recipe)
    empty_session.commit()

    row = empty_session.execute("SELECT name, description, servings FROM recipe").fetchone()
    assert row == ("Grilled Cheese", "Simple sandwich", "1")


def test_recipe_links_to_author_and_category(empty_session):
    author = Author(3, "Nigella Lawson")
    category = Category("Dessert", category_id=3)
    recipe = Recipe(
        recipe_id=2,
        name="Chocolate Cake",
        author=author,
        cook_time=30,
        preparation_time=15,
        created_date=datetime.utcnow(),
        description="Rich chocolate cake",
        category=category,
        rating=5,
        servings="8",
        recipe_yield="1 cake",
    )

    empty_session.add(recipe)
    empty_session.commit()

    retrieved = empty_session.query(Recipe).first()
    assert retrieved.author.name == "Nigella Lawson"
    assert retrieved.category.name == "Dessert"


# ---------------- REVIEW TESTS ----------------

def test_add_and_retrieve_review(empty_session):
    author = Author(4, "Ina Garten")
    category = Category("Breakfast", category_id=4)
    user = User("Reviewer", "pw")
    recipe = Recipe(
        recipe_id=3,
        name="Avocado Toast",
        author=author,
        cook_time=5,
        preparation_time=2,
        created_date=datetime.utcnow(),
        description="Quick snack",
        category=category,
        rating=4,
        servings="1",
        recipe_yield="1 toast",
    )
    review = Review(username="Reviewer", recipe=recipe, rating=5, review="Tasty!", date=datetime.utcnow())

    empty_session.add(user)
    empty_session.add(recipe)
    empty_session.add(review)
    empty_session.commit()

    row = empty_session.execute("SELECT username, recipe_id, rating, review FROM review").fetchone()
    assert row == ("Reviewer", 3, 5, "Tasty!")


# ---------------- FAVORITE TESTS ----------------

def test_add_and_retrieve_favorite(empty_session):
    author = Author(5, "Chef John")
    category = Category("Brunch", category_id=5)
    user = User("Frank", "secret")
    recipe = Recipe(
        recipe_id=4,
        name="Eggs Benedict",
        author=author,
        cook_time=15,
        preparation_time=10,
        created_date=datetime.utcnow(),
        description="Brunch special",
        category=category,
        rating=4.8,
        servings="2",
        recipe_yield="2 servings",
    )
    fav = Favourite(username="Frank", recipe=recipe, favourite_id=None)

    empty_session.add(user)
    empty_session.add(recipe)
    empty_session.add(fav)
    empty_session.commit()

    row = empty_session.execute("SELECT username, id FROM favorite").fetchone()
    # `id` in your ORM refers to Recipe.id (not PK)
    assert row == ("Frank", 4)


def test_favorite_links_user_and_recipe(empty_session):
    author = Author(6, "Test Chef")
    category = Category("Snack", category_id=6)
    user = User("AliceFav", "pw123")
    recipe = Recipe(
        recipe_id=6,
        name="Toastie",
        author=author,
        cook_time=5,
        preparation_time=2,
        created_date=datetime.utcnow(),
        description="Cheese toast",
        category=category,
        rating=4,
        servings="1",
        recipe_yield="1 sandwich",
    )
    fav = Favourite(username="AliceFav", recipe=recipe, favourite_id=None)

    empty_session.add(user)
    empty_session.add(recipe)
    empty_session.add(fav)
    empty_session.commit()

    fav_obj = empty_session.query(Favourite).one()
    assert fav_obj.recipe.name == "Toastie"
    assert fav_obj.username == "AliceFav"


# ---------------- NUTRITION TESTS ----------------

def test_add_and_retrieve_nutrition(empty_session):
    author = Author(7, "Health Chef")
    category = Category("Healthy", category_id=7)
    recipe = Recipe(
        recipe_id=7,
        name="Salad Bowl",
        author=author,
        cook_time=0,
        preparation_time=5,
        created_date=datetime.utcnow(),
        description="Fresh greens",
        category=category,
        rating=4.2,
        servings="2",
        recipe_yield="1 bowl",
    )

    nutrition = Nutrition(
        id=7,
        calories=180,
        fat=5,
        saturated_fat=1,
        cholesterol=0,
        sodium=200,
        carbohydrates=10,
        fiber=2,
        sugar=3,
        protein=6,
    )

    recipe.nutrition = nutrition

    empty_session.add(recipe)
    empty_session.add(nutrition)
    empty_session.commit()

    row = empty_session.execute("SELECT calories, protein FROM nutrition").fetchone()
    assert row == (180.0, 6.0)
