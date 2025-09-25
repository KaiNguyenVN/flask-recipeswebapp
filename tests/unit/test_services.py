from datetime import datetime

import pytest
import tests.conftest
from recipe import MemoryRepository
from recipe.authentication.services import AuthenticationException
from recipe.authentication import services as auth_services
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.review import Review
from recipe.recipe_detail import services as recipe_services
from recipe.favorites import services as favorite_services
from recipe.search_function.services import SearchService
from recipe.domainmodel.user import User
from recipe.recipe_detail.services import ReviewException, FavouriteException


@pytest.fixture
def user():
    return User("alice", "Pw123456")

@pytest.fixture
def other_user():
    return User("bob", "Pw123456")


# Small helper so the tests work whether favourites are
# exposed as a property (list) or a method returning a list.
def _fav_list(u: User):
    attr = getattr(u, "get_favourite_recipes", None)
    if callable(attr):
        return attr()
    return attr


# ----------------- Authentication -----------------
def test_can_add_user(in_memory_repo, user):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user = auth_services.get_user(new_user_name, in_memory_repo)
    assert user.username == new_user_name

    # Check that password has been encrypted.
    assert any(user.password.startswith(prefix) for prefix in ("pbkdf2:sha256:", "scrypt:"))


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'jz'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)

# ----------------- recipe_detail -----------------

def test_add_review_happy_path(repo, user, sample_recipe):
    repo.add_user(user)
    repo.add_recipe(sample_recipe)

    review = recipe_services.add_review(
        user.username,
        recipe_id=sample_recipe.id,
        review_text="Great!",
        rating=5,
        date=datetime.now(),
        repo = repo
    )

    # Returned object is a Review and it is attached to the recipe
    assert isinstance(review, Review)
    assert review in sample_recipe.reviews
    assert review.username == "alice"
    assert review.recipe_id == sample_recipe.id
    assert review.rating == 5
    assert review.review == "Great!"
    assert  sample_recipe.reviews[0].review == "Great!"
    assert sample_recipe.reviews[0].rating == 5
    assert sample_recipe.rating == 5.0


def test_add_review_missing_user_or_recipe_raises(repo, user, sample_recipe):
    # No user added
    repo.add_recipe(sample_recipe)
    with pytest.raises(ReviewException):
        recipe_services.add_review("alice", sample_recipe.id, "ok", 5, datetime.now(), repo)

    # No recipe added
    repo = MemoryRepository()
    repo.add_user(user)
    with pytest.raises(ReviewException):
        recipe_services.add_review("alice", sample_recipe.id, "ok", 5, datetime.now(), repo)


"""
def test_remove_review_happy_path(repo, user, sample_recipe):
    repo.add_user(user)
    repo.add_recipe(sample_recipe)

    r = recipe_services.add_review(user.username, sample_recipe.id, "Nice", 5, datetime.now(), repo)

    removed = recipe_services.remove_review(
        username=user.username,
        recipe_id=sample_recipe.id,
        review_id=r.review_id,
        repo=repo,
    )

    assert removed == r
    assert r not in sample_recipe.reviews  # gone from recipe list


def test_remove_review_wrong_user_raises(repo, user, other_user, sample_recipe):
    repo.add_user(user)
    repo.add_user(other_user)
    repo.add_recipe(sample_recipe)

    r = recipe_services.add_review(user.username, sample_recipe.id, "Nice", 5, datetime.now(), repo)

    with pytest.raises(ReviewException):
        recipe_services.remove_review(
            username=other_user.username,  # not the owner
            recipe_id=sample_recipe.id,
            review_id=r.review_id,
            repo=repo,
        )


def test_remove_review_missing_recipe_raises(repo, user, sample_recipe):
    repo.add_user(user)
    # recipe not added to repo
    with pytest.raises(ReviewException):
        recipe_services.remove_review(user.username, sample_recipe.id, 999, repo)
"""

def test_get_reviews_for_recipe_lists_reviews(repo, user, sample_recipe):
    repo.add_user(user)
    repo.add_recipe(sample_recipe)

    assert recipe_services.get_reviews_for_recipe(sample_recipe.id, repo) == []

    r1 = recipe_services.add_review(user.username, sample_recipe.id, "A", 5, datetime.now(), repo)
    r2 = recipe_services.add_review(user.username, sample_recipe.id, "B", 4, datetime.now(), repo)

    reviews = recipe_services.get_reviews_for_recipe(sample_recipe.id, repo)
    assert r1 in reviews and r2 in reviews
    assert len(reviews) == 2


def test_add_favorite_recipe_happy_path(repo, user, sample_recipe):
    repo.add_user(user)
    repo.add_recipe(sample_recipe)

    fav = recipe_services.add_favorite_recipe(user.username, sample_recipe.id, repo)
    assert isinstance(fav, Favourite)

    favs = _fav_list(user)
    assert favs is not None
    assert fav in favs

def test_add_favorite_recipe_missing_user_or_recipe_raises(repo, user, sample_recipe):
    # No user
    repo.add_recipe(sample_recipe)
    with pytest.raises(FavouriteException):
        recipe_services.add_favorite_recipe(user.username, sample_recipe.id, repo)

    # No recipe
    repo2 = MemoryRepository()
    repo2.add_user(user)
    with pytest.raises(FavouriteException):
        recipe_services.add_favorite_recipe(user.username, sample_recipe.id, repo2)

def test_remove_favorite_recipe_happy_path(repo, user, sample_recipe):
    repo.add_user(user)
    repo.add_recipe(sample_recipe)

    fav = recipe_services.add_favorite_recipe(user.username, sample_recipe.id, repo)
    favs = _fav_list(user)
    assert fav in favs

    recipe_services.remove_favorite_recipe(user.username, sample_recipe.id, repo)
    favs_after = _fav_list(user)
    assert fav not in favs_after


def test_remove_favorite_recipe_missing_user_or_recipe_raises(repo, user, sample_recipe):
    # No user
    repo.add_recipe(sample_recipe)
    with pytest.raises(FavouriteException):
        recipe_services.remove_favorite_recipe(user.username, sample_recipe.id, repo)

    # No recipe
    repo2 = MemoryRepository()
    repo2.add_user(user)
    with pytest.raises(FavouriteException):
        recipe_services.remove_favorite_recipe(user.username, sample_recipe.id, repo2)


# ----------------- favorite -----------------

def test_get_favourite_recipes(user, repo,sample_recipe):
    repo.add_user(user)
    fav = Favourite(user.username, sample_recipe.id, sample_recipe.id)
    user.add_favourite_recipe(fav)
    recipes = favorite_services.get_favourite_recipes(user.username, repo)
    assert len(recipes) == 1
    assert recipes[0] == 38


# ----------------- search_function -----------------

def test_search_by_name_filter(search_service):
    out = search_service.search_recipes(query="Chocolate", filter_by="name")
    names = [r.name for r in out["recipes"]]
    assert names == ["Chocolate Cake"]
    assert out["total_recipes"] == 1
    assert "names" in out["suggestions"]
    assert "Chocolate Cake" in out["suggestions"]["names"]


def test_search_by_ingredients_default(search_service):
    out = search_service.search_recipes(query="lettuce", filter_by="")
    ids = [r.id for r in out["recipes"]]
    assert ids == [3]
    assert out["total_recipes"] == 1


def test_search_with_filter_category(search_service):
    out = search_service.search_recipes(query="Main Course", filter_by="category")
    names = [r.name for r in out["recipes"]]
    assert set(names) == {"Beef Stew", "Salad Bowl"}
    assert names == sorted(names)


def test_pagination_fields_and_counts(search_service):
    out = search_service.search_recipes(query="", filter_by="", page=2, per_page=2)
    p = out["pagination"]
    assert p["page"] == 2
    assert p["has_prev"] is True
    assert p["has_next"] is False
    assert p["prev_page"] == 1
    assert p.get("next_page") in (None, 2)
    assert len(out["recipes"]) == 1


def test_suggestions_structure(search_service):
    out = search_service.search_recipes(query="", filter_by="")
    s = out["suggestions"]
    assert set(s.keys()) >= {"names", "authors", "categories", "ingredients"}
    assert "Chocolate Cake" in s["names"]
    assert "Chef John" in s["authors"]
    assert "Main Course" in s["categories"]
    assert "lettuce" in s["ingredients"]


def test_empty_query_returns_all(search_service):
    out = search_service.search_recipes(query="", filter_by="")
    assert out["total_recipes"] == 3
    assert {r.name for r in out["recipes"]} == {"Chocolate Cake", "Beef Stew", "Salad Bowl"}