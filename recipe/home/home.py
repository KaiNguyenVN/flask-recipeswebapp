from flask import render_template, Blueprint

from recipe.adapters.memory_repository import repo_instance as repo

list_of_recipes = repo.get_recipes()
list_of_categories = repo.get_categories()

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    # Find Nutrition for this recipe
    recipes = repo.get_recipes()
    for recipe in recipes:
        nutrition = repo.get_nutrition_by_recipe_id(recipe.id)
        health_stars = {recipe.id: repo.get_nutrition_by_recipe_id(recipe.id).calculate_health_stars() for recipe in list_of_recipes}

    return render_template('home.html', recipes=list_of_recipes[:6], categories=list_of_categories, nutrition=nutrition, health_stars=health_stars)
