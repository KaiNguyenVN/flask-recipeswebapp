import pytest
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from recipe.domainmodel.user import User
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.category import Category
from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.favourite import Favourite


# ---------------------- HELPER INSERTS ----------------------

def insert_user(empty_session, values=None):
    username, password = values or ("Alice", "Password123")
    empty_session.execute(
        "INSERT INTO user (username, password) VALUES (:username, :password)",
        {"username": username, "password": password}
    )
    row = empty_session.execute(
        "SELECT username FROM user WHERE username = :username", {"username": username}
    ).fetchone()
    return row[0]


def insert_recipe(empty_session):
    empty_session.execute(
        "INSERT INTO recipe (id, name, author_id, cook_time, preparation_time, date, "
        "description, category_id, rating, servings, recipe_yield) "
        "VALUES (1, 'Spaghetti Bolognese', 1, 30, 15, :date, "
        "'Classic Italian dish.', 1, 4.5, '4', '1 pot')",
        {"date": datetime.utcnow()}
    )
    row = empty_session.execute("SELECT id FROM recipe").fetchone()
    return row[0]


def insert_author_and_category(empty_session):
    empty_session.execute(
        "INSERT INTO authors (id, name) VALUES (1, 'Chef Mario')"
    )
    empty_session.execute(
        "INSERT INTO category (id, name) VALUES (1, 'Dinner')"
    )


def insert_review(empty_session, recipe_id, username):
    timestamp = datetime.utcnow()
    empty_session.execute(
        "INSERT INTO review (recipe_id, username, rating, review, date) "
        "VALUES (:recipe_id, :username, 5, 'Amazing dish!', :date)",
        {"recipe_id": recipe_id, "username": username, "date": timestamp}
    )


def insert_favourite(empty_session, recipe_id, username):
    empty_session.execute(
        "INSERT INTO favorite (recipe_id, username) VALUES (:recipe_id, :username)",
        {"recipe_id": recipe_id, "username": username}
    )


# ---------------------- ORM LOADING TESTS ----------------------

def test_loading_of_users(empty_session):
    insert_user(empty_session, ("Bob", "StrongPass"))
    u = empty_session.query(User).one()
    assert u.username == "Bob"
    assert u.password == "StrongPass"


def test_saving_of_user(empty_session):
    user = User("Charlie", "12345")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute("SELECT username, password FROM user"))
    assert rows == [("Charlie", "12345")]


def test_user_duplicate_raises_integrity_error(empty_session):
    insert_user(empty_session, ("Dana", "Secret"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Dana", "Secret")
        empty_session.add(user)
        empty_session.commit()


# ---------------------- RECIPE TESTS ----------------------

def test_loading_of_recipe_with_author_and_category(empty_session):
    insert_author_and_category(empty_session)
    recipe_id = insert_recipe(empty_session)
    recipe = empty_session.query(Recipe).get(recipe_id)

    assert recipe.name == "Spaghetti Bolognese"
    assert recipe.author.name == "Chef Mario"
    assert recipe.category.name == "Dinner"


def test_saving_of_recipe(empty_session):
    author = Author(2, "Julia Child")
    category = Category(2, "Lunch")
    recipe = Recipe(
        recipe_id=2,
        name="Quiche Lorraine",
        author=author,
        cook_time=40,
        preparation_time=20,
        created_date=datetime.utcnow(),
        description="French classic",
        images=[],
        category=category,
        ingredients=["eggs", "cheese"],
        ingredient_quantities=["2", "100g"],
        rating=4.8,
        servings="6",
        recipe_yield="1 pie",
        instructions=["Mix", "Bake"],
        reviews=[]
    )

    empty_session.add(recipe)
    empty_session.commit()

    rows = list(empty_session.execute("SELECT name, description, servings FROM recipe"))
    assert rows == [("Quiche Lorraine", "French classic", "6")]


# ---------------------- REVIEW TESTS ----------------------

def test_loading_of_reviews(empty_session):
    insert_author_and_category(empty_session)
    recipe_id = insert_recipe(empty_session)
    username = insert_user(empty_session)
    insert_review(empty_session, recipe_id, username)

    reviews = list(empty_session.query(Review).all())
    review = reviews[0]

    assert review.username == username
    assert review.recipe.id == recipe_id
    assert review.review == "Amazing dish!"
    assert review.rating == 5


def test_saving_of_review(empty_session):
    author = Author(3, "Nigella Lawson")
    category = Category(3, "Dessert")
    recipe = Recipe(
        recipe_id=3,
        name="Chocolate Cake",
        author=author,
        cook_time=30,
        preparation_time=15,
        created_date=datetime.utcnow(),
        description="Rich chocolate cake",
        images=[],
        category=category,
        ingredients=["flour", "cocoa"],
        ingredient_quantities=["2 cups", "1 cup"],
        rating=5,
        servings="8",
        recipe_yield="1 cake",
        instructions=["Mix", "Bake"],
        reviews=[]
    )

    user = User("Eve", "password")
    review = Review(username="Eve", recipe=recipe, rating=5, review="Perfect!", date=datetime.utcnow())

    empty_session.add(user)
    empty_session.add(recipe)
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute("SELECT username, recipe_id, review, rating FROM review"))
    assert rows == [("Eve", 3, "Perfect!", 5)]


# ---------------------- FAVORITE TESTS ----------------------

def test_saving_and_loading_of_favorite(empty_session):
    insert_author_and_category(empty_session)
    recipe_id = insert_recipe(empty_session)
    username = insert_user(empty_session)

    insert_favourite(empty_session, recipe_id, username)
    favs = list(empty_session.query(Favourite).all())

    assert favs[0].username == username
    assert favs[0].recipe.id == recipe_id


# ---------------------- NUTRITION TESTS ----------------------

def test_saving_of_recipe_with_nutrition(empty_session):
    author = Author(4, "Test Chef")
    category = Category(4, "Health")
    recipe = Recipe(
        recipe_id=4,
        name="Salad",
        author=author,
        cook_time=0,
        preparation_time=10,
        created_date=datetime.utcnow(),
        description="Healthy salad",
        images=[],
        category=category,
        ingredients=["lettuce", "tomato"],
        ingredient_quantities=["2 cups", "1 cup"],
        rating=4.5,
        servings="2",
        recipe_yield="1 bowl",
        instructions=["Mix all"],
        reviews=[]
    )

    nutrition = Nutrition(
        id=4,
        recipe=recipe,
        calories=150,
        fat=5,
        saturated_fat=1,
        cholesterol=10,
        sodium=300,
        carbohydrates=10,
        fiber=2,
        sugar=3,
        protein=5
    )

    empty_session.add(recipe)
    empty_session.add(nutrition)
    empty_session.commit()

    rows = list(empty_session.execute(
        "SELECT calories, fat, protein FROM nutrition WHERE id = 4"
    ))
    assert rows == [(150.0, 5.0, 5.0)]


# ---------------------- RELATIONSHIP ROUNDTRIP ----------------------

def test_user_review_recipe_roundtrip(empty_session):
    author = Author(5, "Jamie Oliver")
    category = Category(5, "Snacks")
    user = User("Frank", "safePass")

    recipe = Recipe(
        recipe_id=5,
        name="Toastie",
        author=author,
        cook_time=5,
        preparation_time=3,
        created_date=datetime.utcnow(),
        description="Quick sandwich",
        images=[],
        category=category,
        ingredients=["bread", "cheese"],
        ingredient_quantities=["2 slices", "1 slice"],
        rating=4,
        servings="1",
        recipe_yield="1 sandwich",
        instructions=["Grill cheese sandwich"],
        reviews=[]
    )

    review = Review(username="Frank", recipe=recipe, rating=4, review="Tasty!", date=datetime.utcnow())
    user.add_review(review)

    empty_session.add(user)
    empty_session.add(recipe)
    empty_session.commit()

    rows = list(empty_session.execute("SELECT username, recipe_id, review FROM review"))
    assert rows == [("Frank", 5, "Tasty!")]
