"""Tests for user login functionality."""
import pytest


@pytest.mark.ui
class TestLogin:
    """Login test suite."""

    @pytest.mark.parametrize(("username", "password"),
        [ pytest.param("admin", "admin", id="admin_user"),#
          pytest.param("user1", "pass1", id="user_1"),
          pytest.param("user2", "pass2", id="user_2"),],)
    def test_successful_login(self, login, username, password):
        """Verify that users can log in with valid credentials."""
        login_page=login(username, password)
        assert login_page.submission_success(), (
            "Login should succeed with valid credentials.")

    @pytest.mark.xfail
    @pytest.mark.parametrize(("username", "password"),
        [pytest.param("admin", "14445", id="invalid_password"),
         pytest.param("00000", "pass1", id="invalid_username"),
         pytest.param("", "pass2", id="empty_username"),],)
    def test_unsuccessful_login(self, login, username, password):
        """Verify that login fails with invalid credentials."""
        login_page=login(username, password)
        assert not login_page.submission_success(), (
            "Login should fail with invalid credentials.")


