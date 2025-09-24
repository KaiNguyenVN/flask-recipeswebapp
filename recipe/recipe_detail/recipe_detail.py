from flask import render_template, Blueprint, redirect, url_for, session, request, flash
from flask_wtf import FlaskForm
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


@recipe_blueprint.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def recipe_detail(recipe_id):
    recipe = repo.repo_instance.get_recipe_by_id(recipe_id)
    if recipe is None:
        return render_template('404.html', message="Recipe not found"), 404

    form = ReviewForm()

    # Store the recipe_id in the hidden field, so it persists across POSTs
    form.recipe_id.data = recipe_id

    if form.validate_on_submit():
        if "user_name" not in session:
            flash("You must be logged in to post a review", "danger")
            return redirect(url_for("authentication_bp.login"))

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

            # Redirect to recipe detail (PRG pattern: Post -> Redirect -> Get)
            return redirect(url_for("recipe_bp.recipe_detail", recipe_id=recipe_id))
        except services.ReviewException as e:
            flash(str(e), "danger")

    # If GET request or failed POST, render recipe detail + form again
    reviews = services.get_reviews_for_recipe(recipe_id, repo.repo_instance)
    return render_template(
        "recipe_detail.html",
        recipe=recipe,
        form=form,
        reviews=reviews,
        handler_url=url_for("recipe_bp.recipe_detail", recipe_id=recipe_id),
    )
