from urllib import request

from flask import render_template, Blueprint, request

from recipe import Recipe
from recipe.adapters.datareader.csvreader import CSVReader
import os

data = CSVReader('recipe/adapters/data/recipes.csv')
data.extract_data()
list_of_recipes = data.get_recipes()
list_of_categories = data.get_categories()

home_blueprint = Blueprint('home_bp', __name__)
browse_blueprint = Blueprint('browse_bp', __name__)
recipe_blueprint = Blueprint('recipe_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('recipeDescription.html', recipes=list_of_recipes[:6], categories=list_of_categories[:6])

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

    return render_template('browse.html', recipes=recipes, categories=list_of_categories, category_images = category_images,
                           page=page, total_pages=total_pages, pages=pages)




@recipe_blueprint.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    # Find recipe by id
    recipe = next((r for r in list_of_recipes if r.id == recipe_id), None)

    if recipe is None:
        # simple 404 fallback
        return render_template('404.html', message="Recipe not found"), 404

    return render_template('recipe_detail.html', recipe=recipe)
