from datetime import datetime
from sqlalchemy import text

from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User

def make_author():
    author = Author(1, 'Bob')
    return author

def make_nutrition() -> Nutrition:
    nutrition = Nutrition(
        id=1,
        calories=250.0,
        fat=10.0,
        saturated_fat=3.0,
        cholesterol=30.0,
        sodium=200.0,
        carbohydrates=30.0,
        fiber=5.0,
        sugar=12.0,
        protein=8.0
    )
    return nutrition

def make_category():
    category = Category('Beverages')
    return category

def make_recipe():
    author = make_author()
    nutrition = make_nutrition()
    recipe = Recipe(5001, 'Test recipe 1', author, 0, 0,
                    datetime(2023, 1, 1), 'Test description', [], "",
                    ['1 cup'], ['flour'], 4.5, nutrition, '4',
                    '1 batch', ['Mix ingredients'])
    return recipe

def insert_recipe(empty_session, recipe):
    empty_session.execute(
        text(
            'INSERT INTO recipes (id, name, author_id, '
            'description, nutrition_id) VALUES '
            f'({recipe.id}, "{recipe.name}", {recipe.author.id}, '
            f'"{recipe.description}", {recipe.nutrition.id})'
        )
    )
    row = empty_session.execute(text('SELECT id FROM recipes ORDER BY id DESC LIMIT 1')).fetchone()
    return row[0]

def insert_author(empty_session, author):
    empty_session.execute(
        text(
            'INSERT INTO authors (id, name) VALUES '
            f'({author.id}, "{author.name}")'
        )
    )
    row = empty_session.execute(text('SELECT id FROM authors ORDER BY id DESC LIMIT 1')).fetchone()
    return row[0]

def test_loading_of_authors(empty_session):
    author = make_author()
    author_key = insert_author(empty_session, author)
    fetched_author = empty_session.query(Author).one()

    assert author_key == fetched_author.id
    assert author == fetched_author

def test_saving_of_author(empty_session):
    author = make_author()
    empty_session.add(author)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT id, name FROM authors')
    ))

    assert rows == [(author.id, author.name)]

def test_loading_of_recipe(empty_session):
    recipe = make_recipe()
    recipe_key = insert_recipe(empty_session, recipe)
    fetched_recipe = empty_session.query(Recipe).one()

    assert recipe_key == fetched_recipe.id
    assert recipe == fetched_recipe

def test_saving_of_recipe(empty_session):
    recipe = make_recipe()
    empty_session.add(recipe)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT id, name, author_id, description, nutrition_id FROM recipes')
    ))

    assert rows == [(
        recipe.id,
        recipe.name,
        recipe.author.id,
        recipe.description,
        recipe.nutrition.id,
    )]

def test_author_recipe_relationship(empty_session):
    author = make_author()
    empty_session.add(author)
    empty_session.commit()

    recipe = make_recipe()
    empty_session.add(recipe)
    empty_session.commit()

    fetched_recipe = empty_session.get(Recipe, recipe.id)

    assert len(fetched_recipe) == 1
    assert fetched_recipe.author.id == author.id

