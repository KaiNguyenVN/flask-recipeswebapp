import math
from flask import request, render_template, Blueprint
import recipe.adapters.repository as abs_repo

from .services import SearchService

search_blueprint = Blueprint('search_bp', __name__)
repo = abs_repo.repo_instance

search_service = SearchService(repo)

@search_blueprint.route("/search")
def search():

    query = request.args.get("q", "").strip()
    filter_by = request.args.get("filter_by", "").strip()
    page = request.args.get("page", 1, type=int)

    search_results = search_service.search_recipes(query, filter_by, page)

    return render_template(
        "search_results.html",
        recipes=search_results['recipes'],
        query=query,
        filter_by=filter_by,
        names=search_results['suggestions']['names'],
        categories=search_results['suggestions']['categories'],
        authors=search_results['suggestions']['authors'],
        ingredients=search_results['suggestions']['ingredients'],
        page=search_results['pagination']['page'],
        total_pages=search_results['pagination']['total_pages'],
        total_recipes=search_results['total_recipes'],
        pages=search_results['pagination']['pages'],
        nutrition=search_results['nutrition'],
        health_stars=search_results['health_stars'],
    )