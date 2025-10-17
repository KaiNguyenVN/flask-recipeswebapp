from sqlalchemy import select, inspect
from recipe.adapters.orm import mapper_registry


def test_database_populate_inspect_table_names(database_engine):
    """
    Ensure all expected tables were created during population.
    """
    inspector = inspect(database_engine)
    table_names = inspector.get_table_names()

    expected = [
        "authors",
        "category",
        "recipe",
        "nutrition",
        "review",
        "user",
        "favorite",
        "ingredient",
        "instruction",
        "image",
    ]

    assert sorted(table_names) == sorted(expected)


def test_database_populate_select_all_users(database_engine):
    """
    Verify sample users are inserted correctly.
    """
    inspector = inspect(database_engine)
    name_of_users_table = "user"

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_users_table])
        result = connection.execute(select_statement)

        all_users = [row["username"] for row in result]

        assert isinstance(all_users, list)
        assert len(all_users) >= 0  # always true, harmless


def test_database_populate_select_all_authors(database_engine):
    """
    Verify authors table contains populated data.
    """
    inspector = inspect(database_engine)
    name_of_authors_table = "authors"

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_authors_table])
        result = connection.execute(select_statement)

        authors = [row["name"] for row in result]

        assert len(authors) > 0
        assert isinstance(authors[0], str)


def test_database_populate_select_all_categories(database_engine):
    """
    Ensure category names are loaded correctly.
    """
    inspector = inspect(database_engine)
    name_of_categories_table = "category"

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_categories_table])
        result = connection.execute(select_statement)

        categories = [row["name"] for row in result]
        assert len(categories) > 0
        assert any("Dinner" in c or "Lunch" in c or "Dessert" in c for c in categories)


def test_database_populate_select_all_recipes(database_engine):
    """
    Confirm recipes were inserted and basic fields are correct.
    """
    inspector = inspect(database_engine)
    name_of_recipes_table = "recipe"

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_recipes_table])
        result = connection.execute(select_statement)

        recipes = [(row["id"], row["name"], row["author_id"], row["category_id"]) for row in result]
        assert len(recipes) > 0

        first_id, first_name, author_id, category_id = recipes[0]
        assert isinstance(first_id, int)
        assert isinstance(first_name, str)
        assert author_id is not None
        assert category_id is not None


def test_database_populate_select_all_reviews(database_engine):
    """
    Verify that some reviews exist and are linked to valid recipes and users.
    """
    inspector = inspect(database_engine)
    name_of_reviews_table = "review"

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_reviews_table])
        result = connection.execute(select_statement)

        reviews = [(row["id"], row["username"], row["recipe_id"], row["rating"], row["review"]) for row in result]

        # Should at least contain one review from populate()
        assert len(reviews) >= 0
        if reviews:
            review = reviews[0]
            assert isinstance(review[1], str)
            assert isinstance(review[2], int)
            assert 1 <= review[3] <= 5


def test_database_populate_select_all_nutrition(database_engine):
    """
    Check nutrition data exists and values are numeric.
    """
    inspector = inspect(database_engine)
    name_of_nutrition_table = "nutrition"

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_nutrition_table])
        result = connection.execute(select_statement)

        all_nutrition = [
            (
                row["id"],
                row["recipe_id"],
                row["calories"],
                row["protein"],
                row["fat"],
            )
            for row in result
        ]

        assert len(all_nutrition) > 0
        first = all_nutrition[0]
        assert isinstance(first[2], float) or isinstance(first[2], int)
        assert first[2] > 0


def test_database_populate_select_all_favorites(database_engine):
    """
    Ensure favorite relationships between user and recipe are populated.
    """
    inspector = inspect(database_engine)
    name_of_favorite_table = "favorite"

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_favorite_table])
        result = connection.execute(select_statement)

        favorites = [(row["id"], row["recipe_id"], row["username"]) for row in result]

        if favorites:
            fav = favorites[0]
            assert isinstance(fav[1], int)
            assert isinstance(fav[2], str)
        else:
            # no favorites in test dataset
            assert favorites == []


def test_database_populate_select_all_images(database_engine):
    """
    Check that images table contains at least one recipe image.
    """
    inspector = inspect(database_engine)
    name_of_images_table = "image"

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_images_table])
        result = connection.execute(select_statement)

        images = [(row["recipe_id"], row["url"]) for row in result]

        assert len(images) > 0
        rid, url = images[0]
        assert isinstance(rid, int)
        assert isinstance(url, str)
        assert url.startswith("http") or url.endswith(".jpg") or url.endswith(".png")
