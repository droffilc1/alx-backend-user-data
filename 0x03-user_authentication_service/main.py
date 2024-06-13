#!/usr/bin/env python3
"""main module
Implements end-to-end integration test
"""
import requests

BASE_URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """Registers a user with the given email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body, timeout=10)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=body, timeout=10)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Logs in with a wrong password and
    verifies that the response status code is 401.
    Args:
        email (str): The email for logging in.
        password (str): The wrong password for logging in.
    Returns:
        None
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body, timeout=10)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in with the given email and password
    and returns the session ID cookie.
    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID cookie.
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body, timeout=10)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Function to perform an unlogged user profile access
    and verify the expected failure.
    No parameters are taken, and the function returns None.
    """
    url = "{}/profile".format(BASE_URL)
    res = requests.get(url, timeout=10)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Function to log the profile access after a successful login.

    Args:
        session_id (str): The session ID for the user.

    Returns:
        None
    """
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(url, cookies=req_cookies, timeout=10)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """
    Logs out the user by deleting the
    session identified by the given session_id.

    Args:
        session_id (str): The unique identifier of the session to be deleted.

    Returns:
        None
    """
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(url, cookies=req_cookies, timeout=10)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Function to reset the password token for a given email.

    Args:
        email (str): The email for which the password reset token is requested.

    Returns:
        str: The reset password token.
    """
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    res = requests.post(url, data=body, timeout=10)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update a user's password using the provided email,
    reset token, and new password.

    Args:
        email (str): The user's email address.
        reset_token (str): The token used to reset the user's password.
        new_password (str): The new password to be set for the user.

    Returns:
        None
    """
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url, data=body, timeout=10)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
