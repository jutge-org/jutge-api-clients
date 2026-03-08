import pytest
import jutge_api_client as j


import re


def test_login_success():
    jutge = j.JutgeApiClient()
    creds = jutge.login("user1@jutge.org", "setzejutges")
    assert isinstance(creds, j.CredentialsOut)
    assert isinstance(creds.token, str)
    assert len(creds.token) > 0
    assert re.fullmatch(r"[0-9a-f]{32}", creds.user_uid)
    assert creds.error == ""


def test_login_failure():
    jutge = j.JutgeApiClient()
    with pytest.raises(j.UnauthorizedException):
        jutge.login("user1@jutge.org", "wrongpassword")


def test_login_with_username():
    jutge = j.JutgeApiClient()
    creds = jutge.auth.login_with_username(
        j.CredentialsWithUsernameIn(username="user1", password="setzejutges")
    )
    assert isinstance(creds, j.CredentialsOut)
    assert isinstance(creds.token, str)
    assert len(creds.token) > 0
    assert re.fullmatch(r"[0-9a-f]{32}", creds.user_uid)
    assert creds.error == ""


def test_logout():
    jutge = j.JutgeApiClient()
    jutge.login("user1@jutge.org", "setzejutges")
    # Verify we're logged in by making an authenticated call
    profile = jutge.student.profile.get()
    assert re.fullmatch(r"[0-9a-f]{32}", profile.user_uid)
    # Logout
    jutge.logout(silent=True)
    # Verify we're logged out
    with pytest.raises(j.UnauthorizedException):
        jutge.student.profile.get()
