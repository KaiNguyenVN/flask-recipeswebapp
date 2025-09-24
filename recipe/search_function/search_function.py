import math

from flask import request, render_template, Blueprint
from recipe.adapters.memory_repository import repo_instance as repo

search_blueprint = Blueprint('search_bp', __name__)

@search_blueprint.route("/search")
def search():

    # get query parameters
    query = request.args.get("q", "").strip()
    filter_by = request.args.get("filter_by", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 12

    # get all recipes from repo
    all_recipes = repo.get_recipes()

    # prepare suggestions for autocomplete
    names = sorted({r.name for r in all_recipes})
    categories = sorted({r.category.name for r in all_recipes})
    authors = sorted({r.author.name for r in all_recipes})
    ingredients = sorted({ing for r in all_recipes for ing in getattr(r, "ingredients", [])})

    # filter and sort recipes
    if filter_by:
        # if query exists → filter accordingly
        if query:
            if filter_by == "name":
                matched_recipes = [r for r in all_recipes if query.lower() in r.name.lower()]
            elif filter_by == "category":
                matched_recipes = [r for r in all_recipes if query.lower() in r.category.name.lower()]
            elif filter_by == "author":
                matched_recipes = [r for r in all_recipes if query.lower() in r.author.name.lower()]
            elif filter_by == "ingredients":
                matched_recipes = [r for r in all_recipes if any(query.lower() in i.lower() for i in r.ingredients)]

        # if no query → just sort all recipes by filter
        else:
            if filter_by == "name":
                matched_recipes = sorted(all_recipes, key=lambda r: r.name.lower())
            elif filter_by == "category":
                matched_recipes = sorted(all_recipes, key=lambda r: r.category.name.lower())
            elif filter_by == "author":
                matched_recipes = sorted(all_recipes, key=lambda r: r.author.name.lower())
            elif filter_by == "ingredients":
                matched_recipes = sorted(all_recipes, key=lambda r: r.ingredients[0].lower() if r.ingredients else "")

    # no filter → show all recipes alphabetically by name
    else:
        matched_recipes = sorted(all_recipes, key=lambda r: r.name.lower())

    # pagination
    total_recipes = len(matched_recipes)
    total_pages = max(1, math.ceil(total_recipes / per_page))
    start = (page - 1) * per_page
    end = start + per_page
    recipes_to_show = matched_recipes[start:end]

    # limit displayed pages
    max_display = 5
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)
    if end_page - start_page < max_display - 1:
        start_page = max(1, end_page - (max_display - 1))
    pages = range(start_page, end_page + 1)

    # Find Nutrition for this recipe
    health_stars = {}
    for recipe in recipes_to_show:
        nutrition = repo.get_nutrition_by_recipe_id(recipe.id)
        if nutrition:
            health_stars[recipe.id] = nutrition.calculate_health_stars()
        else:
            health_stars[recipe.id] = None

    return render_template(
        "search_results.html",
        recipes=recipes_to_show,
        query=query,
        filter_by=filter_by,
        names=names,
        categories=categories,
        authors=authors,
        ingredients=ingredients,
        page=page,
        total_pages=total_pages,
        total_recipes=total_recipes,
        pages=pages,
        nutrition=nutrition,
        health_stars=health_stars,
    )
