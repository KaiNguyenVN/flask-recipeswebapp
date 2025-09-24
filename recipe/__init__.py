"""Initialize Flask app."""
from flask import Flask
from recipe.adapters.memory_repository import repo_instance as repo


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    with app.app_context():
        from recipe.home.home import home_blueprint
        from recipe.browse.browse import browse_blueprint
        from recipe.recipe_detail.recipe_detail import recipe_blueprint
        from recipe.search_function.search_function import search_blueprint

        app.register_blueprint(home_blueprint)
        app.register_blueprint(browse_blueprint)
        app.register_blueprint(recipe_blueprint)
        app.register_blueprint(search_blueprint)

        # Provides full lists of recipes for search suggestions
        @app.context_processor
        def inject_search_data():
            recipes = repo.get_recipes()
            categories = sorted({r.category.name for r in recipes})
            names = sorted({r.name for r in recipes})
            authors = sorted({r.author.name for r in recipes})
            ingredients = sorted({ing for r in recipes for ing in getattr(r, "ingredients", [])})

            return dict(categories=categories, names=names, authors=authors, ingredients=ingredients)

    return app

