from flask import render_template, Blueprint

import recipe.adapters.repository as repo
from recipe.home import services

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    # Find Nutrition for this recipe
    health_stars = {}
    list_of_recipes = services.get_recipes(2,3, "s", repo.repo_instance)
    list_of_categories = list(services.get_categories(repo.repo_instance).values())
    for recipe in list_of_recipes[:6]:  # only first 6 for home page
        nutrition = services.get_nutrition_by_recipe_id(recipe.id, repo.repo_instance)
        if nutrition:
            health_stars[recipe.id] = nutrition.calculate_health_stars()
        else:
            health_stars[recipe.id] = None

    return render_template('home.html', recipes=list_of_recipes[:6], categories=list_of_categories, nutrition=nutrition, health_stars=health_stars)
