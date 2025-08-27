from flask import render_template, Blueprint
from recipe.adapters.data.memory_repository import *

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('recipeDescription.html', recipes=recipes[:4], categories=categories[4:7])