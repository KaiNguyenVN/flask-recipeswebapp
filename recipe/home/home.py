from flask import render_template, Blueprint

from recipe.adapters.memory_repository import repo_instance as repo

list_of_recipes = repo.get_recipes()
list_of_categories = repo.get_categories()

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('recipeDescription.html', recipes=list_of_recipes[:6], categories=list_of_categories[:6])
