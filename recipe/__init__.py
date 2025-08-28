"""Initialize Flask app."""
from flask import Flask




def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    with app.app_context():
        from recipe.home.home import home_blueprint
        from recipe.browse.browse import browse_blueprint
        from recipe.recipe_detail.recipe_detail import recipe_blueprint

        app.register_blueprint(home_blueprint)
        app.register_blueprint(browse_blueprint)
        app.register_blueprint(recipe_blueprint)

    return app
