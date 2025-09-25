from flask import render_template, Blueprint, session, request
from recipe.favorites import services
import recipe.adapters.repository as repo

favorite_blueprint = Blueprint('favorite_bp', __name__)

@favorite_blueprint.route('/favorite', methods=['GET'])
def favorite():
    fav_recipes = services.get_favourite_recipes(username=session["user_name"], repo = repo.repo_instance)
    # sort recipes by name
    sorted_recipes = sorted(fav_recipes, key=lambda r: r.name.lower())


    # pagination
    page = request.args.get('page', 1, type=int)
    per_page = 12
    all_recipes = fav_recipes
    start = (page - 1) * per_page
    end = start + per_page
    recipes = sorted_recipes[start:end]
    total_pages = (len(all_recipes) + per_page - 1) // per_page

    # limit displayed pages
    max_display = 5
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)
    if end_page - start_page < max_display - 1:
        start_page = max(1, end_page - (max_display - 1))
    pages = range(start_page, end_page + 1)

    # Find Nutrition for this recipe
    health_stars = {}
    for recipe in fav_recipes:
        nutrition = repo.repo_instance.get_nutrition_by_recipe_id(recipe.id)
        if nutrition:
            health_stars[recipe.id] = nutrition.calculate_health_stars()
        else:
            health_stars[recipe.id] = None

    return render_template('favorite.html', recipes=recipes,
                           page=page, total_pages=total_pages, pages=pages, health_stars=health_stars)