"""Initialize Flask app."""
from flask import Flask
from pathlib import Path
import recipe.adapters.repository as repo
from recipe.adapters.memory_repository import MemoryRepository
from recipe.authentication.authentication import authentication_blueprint


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = Path('recipe/adapters/data/recipes.csv')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    repo.repo_instance.retrieve_csv_data(data_path)

    with app.app_context():
        from recipe.home.home import home_blueprint
        from recipe.browse.browse import browse_blueprint
        from recipe.recipe_detail.recipe_detail import recipe_blueprint
        from recipe.authentication.authentication import authentication_blueprint

        app.register_blueprint(home_blueprint)
        app.register_blueprint(browse_blueprint)
        app.register_blueprint(recipe_blueprint)
        app.register_blueprint(authentication_blueprint)

    return app
