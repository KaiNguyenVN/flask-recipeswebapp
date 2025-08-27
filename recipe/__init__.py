"""Initialize Flask app."""
from flask import Flask




def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)
    return app
