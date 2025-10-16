from sqlalchemy import select, inspect

from recipe import mapper_registry
from recipe.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    tables = inspector.get_table_names()

    # Check all required tables are there
    assert 'recipes' in tables
    assert 'authors' in tables
    assert 'categories' in tables
    assert 'nutrition' in tables
    assert 'users' in tables
    assert 'reviews' in tables

    assert inspector.get_table_names() == ['recipes', 'authors', 'categories', 'nutrition', 'users', 'reviews']

def test_database_populate_all_recipes(database_engine):
    # Get table information
    inspector = inspect(database_engine)

    # recipes table is at index 6 alphabetically
    recipes_table_name = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table recipes
        select_statement = select(mapper_registry.metadata.tables[recipes_table_name])
        result = connection.execute(select_statement)

        recipes = []
        for row in result:
            recipes.append((row[0], row[1]))

        nr_recipes = len(recipes)
        assert nr_recipes == 13

        # First row is recipe '' with recipe_id
        assert recipes[0] == (38, 'Low-Fat Berry Blue Frozen Dessert')

def test_database_populate_all_authors(database_engine):
    inspector = inspect(database_engine)
    authors_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[authors_table_name])
        result = connection.execute(select_statement)

        authors = []
        for row in result:
            authors.append((row[2], row[3]))

        nr_authors = len(authors)
        assert nr_authors == 13

        assert authors[0] == (1533, 'Dancer')

def test_database_populate_all_categories(database_engine):
    inspector = inspect(database_engine)
    authors_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[authors_table_name])
        result = connection.execute(select_statement)

        categories = []
        for row in result:
            categories.append((row[10]))

        nr_categories = len(categories)
        assert nr_categories == 13

        assert categories[0] == 'Frozen Desserts'

def test_database_populate_all_nutrients(database_engine):
    inspector = inspect(database_engine)
    authors_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[authors_table_name])
        result = connection.execute(select_statement)

        nutrients = []
        for row in result:
            nutrients.append((row[0], row[13], row[14], row[15], row[16], row[17]))

        nr_nutrients = len(nutrients)
        assert nr_nutrients == 13

        assert nutrients[0] == (38, 170.9, 2.5, 1.3, 8.0, 29.8)

def test_database_populate_all_users(database_engine):
    inspector = inspect(database_engine)
    authors_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[authors_table_name])
        result = connection.execute(select_statement)

        authors = []
        for row in result:
            authors.append((row[2], row[3]))

        nr_authors = len(authors)
        assert nr_authors == 13

        assert authors[0] == (1533, 'Dancer')

def test_database_populate_all_reviews(database_engine):
    inspector = inspect(database_engine)
    authors_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[authors_table_name])
        result = connection.execute(select_statement)

        authors = []
        for row in result:
            authors.append((row[2], row[3]))

        nr_authors = len(authors)
        assert nr_authors == 13

        assert authors[0] == (1533, 'Dancer')