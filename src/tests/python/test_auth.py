import pytest
import jutge_api_client as j


USER_UID = "99df26a2d6b44b41ad3772f5525dce52"


def test_login_success():
    jutge = j.JutgeApiClient()
    creds = jutge.login("user1@jutge.org", "setzejutges")
    assert isinstance(creds, j.CredentialsOut)
    assert isinstance(creds.token, str)
    assert len(creds.token) > 0
    assert creds.user_uid == USER_UID
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
    assert creds.user_uid == USER_UID
    assert creds.error == ""


def test_logout():
    jutge = j.JutgeApiClient()
    jutge.login("user1@jutge.org", "setzejutges")
    # Verify we're logged in by making an authenticated call
    profile = jutge.student.profile.get(None)
    assert profile.user_uid == USER_UID
    # Logout
    jutge.logout(silent=True)
    # Verify we're logged out
    with pytest.raises(j.UnauthorizedException):
        jutge.student.profile.get(None)
