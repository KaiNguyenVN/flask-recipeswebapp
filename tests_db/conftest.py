import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from recipe.adapters import database_repository, repository_populate
from recipe.adapters.orm import mapper_registry, map_model_to_tables
from pathlib import Path

# --- Data paths ---
PROJECT_ROOT = Path(__file__).parent.parent
FULL_DATA_PATH = PROJECT_ROOT / "recipe" / "adapters" / "data"
TEST_DATA_PATH = PROJECT_ROOT / "tests" / "data"

# --- Database URIs ---
TEST_DATABASE_URI_FILE = 'sqlite:///recipes-test.db'
TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'


# ----------------------- Persistent file database (LIMITED dataset) ---------------------------
@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)

    # Recreate all tables
    mapper_registry.metadata.create_all(engine)
    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())

    # Map ORM models again
    map_model_to_tables()

    # Create session factory + repository
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    # Populate LIMITED dataset (tests/data/)
    repository_populate.populate(TEST_DATA_PATH, repo_instance, database_mode=True)

    yield engine

    # Cleanup
    mapper_registry.metadata.drop_all(engine)


# ---------------------------In-memory database (FULL dataset)---------------------------
@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)

    mapper_registry.metadata.create_all(engine)
    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())

    map_model_to_tables()

    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    # Populate FULL dataset (recipe/adapters/data/)
    repository_populate.populate(FULL_DATA_PATH, repo_instance, database_mode=True)

    yield session_factory
    mapper_registry.metadata.drop_all(engine)


# --------------------------- Empty database (no data)---------------------------
@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)

    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())

    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)

    yield session_factory()

    mapper_registry.metadata.drop_all(engine)
