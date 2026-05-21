# tests/test_login.py

import pytest
from pages.login_page import Login


@pytest.mark.usefixtures("setup")
class TestLogin:
    def test_login_success(self):
        login_page = Login(self.driver)
        heading = login_page.do_login("7567546456", "789987")
        assert "Dashboard" in heading
        