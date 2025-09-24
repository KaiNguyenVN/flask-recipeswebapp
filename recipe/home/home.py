from flask import render_template, Blueprint

import recipe.adapters.repository as repo

list_of_recipes = repo.repo_instance.get_recipes()
list_of_categories = list(repo.repo_instance.get_categories().values())

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    # Find Nutrition for this recipe
    health_stars = {}
    for recipe in list_of_recipes[:6]:  # only first 6 for home page
        nutrition = repo.get_nutrition_by_recipe_id(recipe.id)
        if nutrition:
            health_stars[recipe.id] = nutrition.calculate_health_stars()
        else:
            health_stars[recipe.id] = None

    return render_template('home.html', recipes=list_of_recipes[:6], categories=list_of_categories, nutrition=nutrition, health_stars=health_stars)
