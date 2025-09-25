from werkzeug.security import generate_password_hash, check_password_hash

from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.user import User


class NameNotUniqueException(Exception):
    pass

class UnknownUserException(Exception):
    pass

class AuthenticationException(Exception):
    pass


def add_user(user_name: str, password: str, repo: AbstractRepository):
    # Check that the given username is available.
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueException
    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    # Create and store the new User, with password encrypted.
    user = User(user_name, password_hash)
    repo.add_user(user)

def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return user

def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False
    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException

