"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db.init_app(app)

    with app.app_context():
        from recipe.home.home import home_blueprint
        from recipe.browse.browse import browse_blueprint
        from recipe.recipe_detail.recipe_detail import recipe_blueprint
        from recipe.search_function.search_function import search_blueprint

        app.register_blueprint(home_blueprint)
        app.register_blueprint(browse_blueprint)
        app.register_blueprint(recipe_blueprint)
        app.register_blueprint(search_blueprint)

    return app
