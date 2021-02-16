from datetime import datetime, timedelta
from functools import wraps
from typing import Union

import jwt
from flask import g
from flask import request

from anubis.config import config
from anubis.models import User
from anubis.utils.data import is_debug
from anubis.utils.http import error_response, get_request_ip


def get_user(netid: Union[str, None]) -> Union[User, None]:
    """
    Load a user by username

    :param netid: netid of wanted user
    :return: User object or None
    """
    if netid is None:
        return None

    # Get the user from the database
    user = User.query.filter_by(netid=netid).first()

    return user


def current_user() -> Union[User, None]:
    """
    Load current user based on the token

    :return: User or None
    """
    if g.get("user", default=None) is not None:
        return g.user

    # Attempt to get the token from the request
    token = get_token()
    if token is None:
        return None

    # Try to decode the jwt
    try:
        decoded = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        return None

    # Make sure there is a netid in the jwt
    if "netid" not in decoded:
        return None

    # Get the user from the decoded jwt
    user = get_user(decoded["netid"])

    # Cache the user in the request context
    g.user = user

    return user


def get_token() -> Union[str, None]:
    """
    Attempt to get the token from the request. Both the cookie, and the
    headers will be checked.

    :return:
    """

    return request.headers.get("token", default=None) or request.cookies.get(
        "token", default=None
    )


def create_token(netid: str, **extras) -> Union[str, None]:
    """
    Get token for user by netid

    :param netid:
    :return: token string or None (if user not found)
    """

    # Get user
    user: User = get_user(netid)

    # Verify user exists
    if user is None:
        return None

    # Create new token
    return jwt.encode(
        {
            "netid": user.netid,
            "exp": datetime.utcnow() + timedelta(hours=6),
            **extras,
        },
        config.SECRET_KEY,
    )


def require_user(unless_debug=False):
    """
    Wrap a function to require a user to be logged in.
    If they are not logged in, they will get an Unathed
    error response with status code 401.

    :param unless_debug:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the user in the current
            # request context.
            user = current_user()

            # Bypass auth if the api is in debug
            # mode and unless_debug is true.
            if unless_debug and is_debug():
                return func(*args, **kwargs)

            # Check that there is a user specified
            # in the current request context, and
            # that use is an admin.
            if user is None:
                return error_response("Unauthenticated"), 401

            # Pass the parameters to the
            # decorated function.
            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_admin(unless_debug=False, unless_vpn=False):
    """
    Wrap a function to require an admin to be logged in.
    If they are not logged in, they will get an Unathed
    error response with status code 401.

    :param unless_debug:
    :param unless_vpn:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the user in the current
            # request context.
            user = current_user()

            # Bypass auth if vpn
            if unless_vpn and get_request_ip() == '128.238.66.211':
                return func(*args, **kwargs)

            # Bypass auth if the api is in debug
            # mode and unless_debug is true.
            if unless_debug and is_debug():
                return func(*args, **kwargs)

            # Check that there is a user specified
            # in the current request context, and
            # that use is an admin.
            if user is None or user.is_admin is False:
                return error_response("Unauthenticated"), 401

            # Pass the parameters to the
            # decorated function.
            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_superuser(unless_debug=False, unless_vpn=False):
    """
    Wrap a function to require an superuser to be logged in.
    If they are not logged in, they will get an Unathed
    error response with status code 401.

    :param unless_debug:
    :param unless_vpn:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the user in the current
            # request context.
            user = current_user()

            # Bypass auth if vpn
            if unless_vpn and get_request_ip() == '128.238.66.211':
                return func(*args, **kwargs)

            # Bypass auth if the api is in debug
            # mode and unless_debug is true.
            if unless_debug and is_debug():
                return func(*args, **kwargs)

            # Check that there is a user specified
            # in the current request context, and
            # that use is a superuser.
            if user is None or user.is_superuser is False:
                return error_response("Unauthenticated"), 401

            # Pass the parameters to the
            # decorated function.
            return func(*args, **kwargs)

        return wrapper

    return decorator
