from flask import render_template, Blueprint
from recipe.adapters.datareader.csvdatareader import list_of_recipes, list_of_categories

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('recipeDescription.html', recipes=list_of_recipes, categories=list_of_categories)