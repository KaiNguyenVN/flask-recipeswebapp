from flask import render_template, Blueprint

import recipe.adapters.repository as repo

list_of_recipes = repo.repo_instance.get_recipes()
list_of_categories = list(repo.repo_instance.get_categories().values())

recipe_blueprint = Blueprint('recipe_bp', __name__)

@recipe_blueprint.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    # Find recipe by id
    recipe = next((r for r in list_of_recipes if r.id == recipe_id), None)

    if recipe is None:
        # simple 404 fallback
        return render_template('404.html', message="Recipe not found"), 404

    return render_template('recipe_detail.html', recipe=recipe)