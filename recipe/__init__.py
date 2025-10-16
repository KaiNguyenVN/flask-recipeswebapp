"""Initialize Flask app."""
from flask import Flask, session
from pathlib import Path
import recipe.adapters.repository as repo
from recipe.adapters import memory_repository, repository_populate, database_repository
from recipe.adapters.memory_repository import MemoryRepository
from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.adapters.orm import metadata, map_model_to_tables, mapper_registry
from recipe.adapters.repository_populate import populate
from recipe.authentication.authentication import authentication_blueprint

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = Path('recipe/adapters/data/recipes.csv')

    # Database and Repository setup
    database_uri = "sqlite:///recipes.db"
    engine = create_engine(database_uri)
    clear_mappers()
    session_factory = sessionmaker(bind=engine)
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    @app.before_request
    def check_session_user():
        user_name = session.get("user_name")
        if user_name and repo.repo_instance.get_user(user_name) is None:
            session.clear()  # invalidate cookie if user no longer exists


    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    database_mode = True

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        repository_populate.populate(data_path, repo.repo_instance, database_mode)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        # Check if database needs to be initialised or reset
        inspector = inspect(database_engine)

        if app.config['TESTING'] == 'True' or len(inspector.get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            mapper_registry.metadata.create_all(database_engine)  # Conditionally create database tables.

            # Clear existing data for a clean start
            with database_engine.connect() as connection:
                for table in reversed(metadata.sorted_tables):
                    connection.execute(table.delete())
                    connection.commit()


            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            repository_populate.populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

    populate(data_path, repo.repo_instance, database_mode)

    with app.app_context():
        from recipe.home.home import home_blueprint
        from recipe.browse.browse import browse_blueprint
        from recipe.recipe_detail.recipe_detail import recipe_blueprint
        from recipe.authentication.authentication import authentication_blueprint
        from recipe.search_function.search_function import search_blueprint
        from recipe.favorites.favorite import favorite_blueprint

        app.register_blueprint(home_blueprint)
        app.register_blueprint(browse_blueprint)
        app.register_blueprint(recipe_blueprint)
        app.register_blueprint(authentication_blueprint)
        app.register_blueprint(search_blueprint)
        app.register_blueprint(favorite_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

        # Provides full lists of recipes for search suggestions
        @app.context_processor
        def inject_search_data():
            recipes = repo.repo_instance.get_recipes(2, 3, "s")
            categories = sorted({r.category.name for r in recipes})
            names = sorted({r.name for r in recipes})
            authors = sorted({r.author.name for r in recipes})
            ingredients = sorted({ing for r in recipes for ing in getattr(r, "ingredients", [])})

            return dict(categories=categories, names=names, authors=authors, ingredients=ingredients)

    return app
