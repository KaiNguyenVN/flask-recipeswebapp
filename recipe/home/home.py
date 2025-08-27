from flask import render_template, Blueprint
from recipe.adapters.memory_repository import repo_instance as repo

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('recipeDescription.html',
                           recipes=repo.get_recipes()[:4],
                           categories=repo.get_categories()[4:7])