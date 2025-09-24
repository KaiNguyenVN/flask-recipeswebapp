import math

from flask import request, redirect, render_template, Blueprint
from recipe.adapters.memory_repository import repo_instance as repo

search_blueprint = Blueprint('search_bp', __name__)

# Search - find recipes based on input
@search_blueprint.route("/search")
def search_page():
    recipes = repo.get_recipes()

    # Collect unique names, categories, authors
    names = sorted({r.name for r in recipes})
    categories = sorted({r.category.name for r in recipes})
    authors = sorted({r.author.name for r in recipes})

    return render_template(
        "search_results.html",
        recipes=[],
        query="",
        names=names,
        categories=categories,
        authors=authors
    )

# Shows recipes based on input
@search_blueprint.route("/search_redirect")
def search_redirect():
    query = request.args.get("q", "").strip().lower()
    filter_by = request.args.get("filter_by", "name")

    recipes = repo.get_recipes()
    matched_recipes = []

    # Find all matches that contain the query
    for r in recipes:
        if filter_by == "name" and query in r.name.lower():
            matched_recipes.append(r)
        elif filter_by == "category" and query in r.category.name.lower():
            matched_recipes.append(r)
        elif filter_by == "author" and query in r.author.name.lower():
            matched_recipes.append(r)
        elif filter_by == "ingredients" and any(query in i.lower() for i in r.ingredients):
            matched_recipes.append(r)

    # Sort alphabetically by name and limit to 10
    matched_recipes.sort(key=lambda r: r.name.lower())

    # If exact match exists on name → redirect
    exact_match = next((r for r in matched_recipes if r.name.lower() == query), None)
    if exact_match:
        return redirect(f"/recipe/{exact_match.id}")

    # Pagination variables
    total_recipes = len(matched_recipes)
    page = int(request.args.get("page", 1))
    per_page = 12
    total_pages = math.ceil(total_recipes / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    recipes_to_show = matched_recipes[start:end]

    return render_template(
        "search_results.html",
        filter_by = filter_by,
        recipes=recipes_to_show,
        query=query,
        page=page,
        total_pages=total_pages,
        total_recipes=total_recipes,
        pages=list(range(1, total_pages + 1))  # simple page list
    )
