from flask import render_template, Blueprint
from recipe.adapters.memory_repository import repo_instance as repo

list_of_recipes = repo.get_recipes()
list_of_categories = repo.get_categories()

recipe_blueprint = Blueprint('recipe_bp', __name__)

@recipe_blueprint.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    # Find recipe by id
    recipe = next((r for r in list_of_recipes if r.id == recipe_id), None)

    if recipe is None:
        # simple 404 fallback
        return render_template('404.html', message="Recipe not found"), 404

    # Find Nutrition for this recipe
    nutrition = repo.get_nutrition_by_recipe_id(recipe_id)
    health_stars = {recipe.id: repo.get_nutrition_by_recipe_id(recipe.id).calculate_health_stars() for recipe in list_of_recipes}

    return render_template('recipe_detail.html', recipe=recipe, nutrition=nutrition, health_stars=health_stars)