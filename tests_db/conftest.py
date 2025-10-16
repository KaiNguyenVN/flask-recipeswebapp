import pytest, sys, os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from recipe.adapters import database_repository, repository_populate
from recipe.adapters.orm import mapper_registry, map_model_to_tables


# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


TEST_DATA_PATH_DATABASE_LIMITED = project_root / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///recipes-test.db'


@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)

    mapper_registry.metadata.create_all(engine)  # Conditionally create database tables.
    # Remove any data from the tables.
    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker
    session_factory = sessionmaker(
        autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    repository_populate.populate(
        TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, database_mode=True)
    yield engine
    mapper_registry.metadata.drop_all(engine)


# Creates a fresh database session for each test
@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    mapper_registry.metadata.create_all(engine)
    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(
        autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    repository_populate.populate(
        TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, database_mode=True)
    yield session_factory
    mapper_registry.metadata.drop_all(engine)


# A database session with empty tables (no data)
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
