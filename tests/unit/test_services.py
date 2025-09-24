import pytest
import tests.conftest
from recipe.authentication.services import AuthenticationException
from recipe.authentication import services as auth_services


def test_can_add_user(in_memory_repo):
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


"""
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Home" in response.data
    assert b"Recipe" in response.data

def test_browse_page(client):
    response = client.get("/browse")
    assert response.status_code == 200
    assert b"browse-list" in response.data
    assert b"browse-card" in response.data

@pytest.mark.parametrize("recipe_id", [1, 2, 3])
def test_recipe_detail_page(client, recipe_id):
    response = client.get(f"/recipe/{recipe_id}")
    if response.status_code == 404:
        assert b"Recipe not found" in response.data
    else:
        assert response.status_code == 200
        assert b"Recipe" in response.data

def test_nonexistent_recipe(client):
    response = client.get("/recipe/99999")
    assert response.status_code == 404
    assert b"Recipe not found" in response.data
"""
