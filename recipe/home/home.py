from flask import render_template, Blueprint

import recipe.adapters.repository as repo

list_of_recipes = repo.repo_instance.get_recipes()
list_of_categories = list(repo.repo_instance.get_categories().values())

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('recipeDescription.html', recipes=list_of_recipes[:6], categories=list_of_categories)
