from sqlalchemy import select, inspect, text

from recipe import mapper_registry

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


def test_database_tables_exist(empty_session):
    # Test that all required tables exist
    tables = ['recipe', 'authors', 'category', 'user', 'review', 'favorite',
              'nutrition', 'ingredient', 'instruction', 'image']

    for table in tables:
        result = empty_session.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"))
        assert result.fetchone() is not None, f"Table {table} does not exist"


def test_tables_are_populated(session_factory):
    from recipe.adapters.database_repository import SqlAlchemyRepository
    repo = SqlAlchemyRepository(session_factory)

    # Test recipes are populated
    recipes = repo.get_all_recipes()
    assert len(recipes) > 0, "Recipes table is not populated"

    # Test authors are populated
    authors = repo.get_authors()
    assert len(authors) > 0, "Authors table is not populated"

    # Test categories are populated
    categories = repo.get_categories()
    assert len(categories) > 0, "Categories table is not populated"


def test_recipe_data_integrity(session_factory):
    from recipe.adapters.database_repository import SqlAlchemyRepository
    repo = SqlAlchemyRepository(session_factory)

    # Test a specific recipe has all required data
    recipe = repo.get_recipe_by_id(9518)  # Use an existing recipe ID

    assert recipe is not None, "Recipe 9518 not found"
    assert recipe.name is not None, "Recipe name is missing"
    assert recipe.author is not None, "Recipe author is missing"
    assert recipe.category is not None, "Recipe category is missing"
    assert len(recipe.ingredients) > 0, "Recipe ingredients are missing"
    assert len(recipe.instructions) > 0, "Recipe instructions are missing"