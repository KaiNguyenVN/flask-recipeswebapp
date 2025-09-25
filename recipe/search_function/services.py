import math
from typing import List, Dict, Any, Tuple
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.nutrition import Nutrition


class SearchService:
    def __init__(self, repository):
        self.repo = repository

    def search_recipes(self, query: str = "", filter_by: str = "", page: int = 1, per_page: int = 12) -> Dict[str, Any]:
        """Search recipes with filtering and pagination"""
        all_recipes = self.repo.get_recipes()

        # Filter recipes
        matched_recipes = self._filter_recipes(all_recipes, query, filter_by)

        # Sort recipes
        matched_recipes = self._sort_recipes(matched_recipes, filter_by)

        # Paginate results
        paginated_recipes, pagination_data = self._paginate_recipes(matched_recipes, page, per_page)

        # Get nutrition and health data
        nutrition_map, health_stars = self._get_nutrition_data(paginated_recipes)

        # Get autocomplete suggestions
        suggestions = self._get_autocomplete_suggestions(all_recipes)

        return {
            'recipes': paginated_recipes,
            'total_recipes': len(matched_recipes),
            'nutrition': nutrition_map,
            'health_stars': health_stars,
            'suggestions': suggestions,
            'pagination': pagination_data
        }

    def _filter_recipes(self, recipes: List[Recipe], query: str, filter_by: str) -> List[Recipe]:
        """Filter recipes based on query and filter type"""
        if not query:
            return recipes

        query_lower = query.lower()

        filter_map = {
            'name': lambda r: query_lower in r.name.lower(),
            'category': lambda r: query_lower in r.category.name.lower(),
            'author': lambda r: query_lower in r.author.name.lower(),
            'ingredients': lambda r: any(query_lower in ing.lower() for ing in getattr(r, 'ingredients', []))
        }

        if filter_by in filter_map:
            return [r for r in recipes if filter_map[filter_by](r)]

        # Default search across multiple fields
        return [r for r in recipes if (
                query_lower in r.name.lower() or
                query_lower in r.category.name.lower() or
                query_lower in r.author.name.lower() or
                any(query_lower in ing.lower() for ing in getattr(r, 'ingredients', []))
        )]

    def _sort_recipes(self, recipes: List[Recipe], filter_by: str) -> List[Recipe]:
        """Sort recipes based on filter type"""
        sort_map = {
            'name': lambda r: r.name.lower(),
            'category': lambda r: r.category.name.lower(),
            'author': lambda r: r.author.name.lower(),
            'ingredients': lambda r: (r.ingredients[0].lower() if getattr(r, 'ingredients', []) else "")
        }

        if filter_by in sort_map:
            return sorted(recipes, key=sort_map[filter_by])

        return sorted(recipes, key=lambda r: r.name.lower())

    def _paginate_recipes(self, recipes: List[Recipe], page: int, per_page: int) -> Tuple[List[Recipe], Dict[str, Any]]:
        """Paginate recipe results"""
        total_recipes = len(recipes)
        total_pages = max(1, math.ceil(total_recipes / per_page))
        page = max(1, min(page, total_pages))

        start = (page - 1) * per_page
        end = start + per_page
        paginated_recipes = recipes[start:end]

        # Calculate pagination range
        max_display = 5
        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)
        if end_page - start_page < max_display - 1:
            start_page = max(1, end_page - (max_display - 1))

        pagination_data = {
            'page': page,
            'total_pages': total_pages,
            'pages': range(start_page, end_page + 1),
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_page': page - 1 if page > 1 else None,
            'next_page': page + 1 if page < total_pages else None
        }

        return paginated_recipes, pagination_data

    def _get_nutrition_data(self, recipes: List[Recipe]) -> Tuple[Dict[int, Nutrition], Dict[int, float]]:
        """Get nutrition data and health stars for recipes"""
        nutrition_map = {}
        health_stars = {}

        for recipe in recipes:
            nutrition = self.repo.get_nutrition_by_recipe_id(recipe.id)
            nutrition_map[recipe.id] = nutrition
            health_stars[recipe.id] = nutrition.calculate_health_stars() if nutrition else None

        return nutrition_map, health_stars

    def _get_autocomplete_suggestions(self, recipes: List[Recipe]) -> Dict[str, List[str]]:
        """Get autocomplete suggestions for search"""
        return {
            'names': sorted({r.name for r in recipes}),
            'categories': sorted({r.category.name for r in recipes}),
            'authors': sorted({r.author.name for r in recipes}),
            'ingredients': sorted({ing for r in recipes for ing in getattr(r, 'ingredients', [])})
        }
