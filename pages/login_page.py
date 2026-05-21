# pages/login_page.py

import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Login:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "login_name")
        self.password_input = (By.ID, "login_pw")
        self.login_button = (By.CSS_SELECTOR, ".btn.btn-primary.login-user")
        self.confirm_button = (By.CSS_SELECTOR, ".btn.btn-primary.confirmSignin")
        self.dashboard_title = (By.CSS_SELECTOR, ".page-title")

    def do_login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
        self.driver.find_element(*self.confirm_button).click()

        heading_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.dashboard_title)
        )
        heading = heading_element.text.strip()

        report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "Medilogin")
        os.makedirs(report_dir, exist_ok=True)
        self.driver.save_screenshot(os.path.join(report_dir, "Login.jpg"))

        return heading
