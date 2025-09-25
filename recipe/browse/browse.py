from urllib import request

from flask import render_template, Blueprint, request

import recipe.adapters.repository as repo

list_of_recipes = repo.repo_instance.get_recipes()
list_of_categories = list(repo.repo_instance.get_categories().values())

browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    category_images = {}

    # sort recipes by name
    sorted_recipes = sorted(list_of_recipes, key=lambda r: r.name.lower())

    for category in list_of_categories:
        for recipe in sorted_recipes:
            # Use singular category attribute
            if hasattr(recipe, 'category') and recipe.category.name == category.name:
                if recipe.images and len(recipe.images) > 0:
                    category_images[category.name] = recipe.images[0]
                else:
                    category_images[category.name] = "https://via.placeholder.com/300x200?text=No+Image"
                break

    # pagination
    page = request.args.get('page', 1, type=int)
    per_page = 12
    all_recipes = list_of_recipes
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
    for recipe in list_of_recipes:
        nutrition = repo.repo_instance.get_nutrition_by_recipe_id(recipe.id)
        if nutrition:
            health_stars[recipe.id] = nutrition.calculate_health_stars()
        else:
            health_stars[recipe.id] = None

    return render_template('browse.html', recipes=recipes, categories=list_of_categories, category_images = category_images,
                           page=page, total_pages=total_pages, pages=pages, health_stars=health_stars)