"""Tests for user login functionality."""
import pytest

@pytest.mark.ui
class TestLogin:
    """Login test suite."""

    def test_successful_login(self, login, valid_user):
        """Verify that users can log in with valid credentials."""
        username, password = valid_user
        login_page=login(username, password)
        assert login_page.submission_success(), (
            "Login should succeed with valid credentials.")

    @pytest.mark.xfail
    def test_unsuccessful_login(self, login, invalid_user):
        """Verify that login fails with invalid credentials."""
        username, password = invalid_user
        login_page=login(username, password)
        assert not login_page.submission_success(), (
            "Login should fail with invalid credentials.")