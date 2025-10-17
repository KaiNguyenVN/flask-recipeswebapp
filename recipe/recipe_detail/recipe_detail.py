from flask import render_template, Blueprint, redirect, url_for, session, request, flash
from flask_wtf import FlaskForm
#from sqlalchemy.testing.suite.test_reflection import users
from wtforms import TextAreaField, IntegerField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime

import recipe.adapters.repository as repo
import recipe.recipe_detail.services as services
from recipe.authentication.authentication import login_required

recipe_blueprint = Blueprint('recipe_bp', __name__)


class ReviewForm(FlaskForm):
    recipe_id = HiddenField("Recipe ID")  # keeps recipe id across GET/POST
    review_text = TextAreaField("Your review", validators=[DataRequired()])
    rating = IntegerField("Rating (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField("Post Review")

# ----------------------Recipe details rendered-------------------------

@recipe_blueprint.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    recipe = repo.repo_instance.get_recipe_by_id(recipe_id)
    list_of_recipes = repo.repo_instance.get_recipes(1, 100, "s")

    if recipe is None:
        return render_template('404.html', message="Recipe not found"), 404

    form = ReviewForm()
    form.recipe_id.data = recipe_id

    # Determine if current user has favorited this recipe
    is_favorited = False
    if "user_name" in session:
        is_favorited = services.is_favorited(
            username=session["user_name"],
            recipe_id=recipe_id,
            repo=repo.repo_instance,
        )

    # Reviews & nutrition
    reviews = services.get_reviews_for_recipe(recipe_id, repo.repo_instance)
    nutrition = repo.repo_instance.get_nutrition_by_recipe_id(recipe_id)
    health_stars = {
        recipe.id: repo.repo_instance.get_nutrition_by_recipe_id(recipe.id).calculate_health_stars()
        for recipe in list_of_recipes
    }

    return render_template(
        "recipe_detail.html",
        recipe=recipe,
        form=form,
        reviews=reviews,
        handler_url=url_for("recipe_bp.add_review", recipe_id=recipe_id),
        nutrition=nutrition,
        health_stars=health_stars,
        is_favorited=is_favorited,
        favorite_handler_url=url_for("recipe_bp.add_favorite", recipe_id=recipe_id),
    )

#---------------------------------Review --------------------------------
@recipe_blueprint.route('/recipe/<int:recipe_id>/add_review', methods=['POST'])
@login_required
def add_review(recipe_id):
    form = ReviewForm()

    # Ensure recipe_id persists
    form.recipe_id.data = recipe_id

    if not form.validate_on_submit():
        flash("Please fill in all fields correctly.", "danger")
        return redirect(url_for("recipe_bp.recipe_detail", recipe_id=recipe_id))

    try:
        services.add_review(
            username=session["user_name"],
            recipe_id=int(form.recipe_id.data),
            review_text=form.review_text.data,
            rating=form.rating.data,
            date=datetime.utcnow(),
            repo=repo.repo_instance,
        )
        flash("Your review has been added!", "success")
    except services.ReviewException as e:
        flash(str(e), "danger")

    # redirect back to recipe detail
    return redirect(url_for("recipe_bp.recipe_detail", recipe_id=recipe_id))

@recipe_blueprint.post('/recipe/<int:recipe_id>/favorite')
@login_required
def add_favorite(recipe_id: int):
    """
    Add the given recipe to the logged-in user's favorites, then redirect back to the detail page.
    """
    try:
        services.add_favorite_recipe(
            username=session["user_name"],
            recipe_id=recipe_id,
            repo=repo.repo_instance,
        )
    except Exception as e:
        # If already in favorites or other domain exceptions, surface an info message.
        msg = str(e) if str(e) else "Already in favorites."
        flash(msg, "info")
    return redirect(url_for("recipe_bp.recipe_detail", recipe_id=recipe_id))

@recipe_blueprint.post('/recipe/<int:recipe_id>/unfavorite')
@login_required
def remove_favorite(recipe_id: int):
    services.remove_favorite_recipe(
        username=session["user_name"],
        recipe_id=recipe_id,
        repo=repo.repo_instance,
    )
    return redirect(url_for("recipe_bp.recipe_detail", recipe_id=recipe_id))
