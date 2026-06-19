import os
from html import escape

import pytest
from Common import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode"
    )


@pytest.fixture(scope="class")
def setup(request):
    options = Options()

    # Run headless only when --headless is passed
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

    driver.maximize_window()
    driver.implicitly_wait(25)
    driver.get("https://stagedoctors.mediquince.com/")

    request.cls.driver = driver

    yield

    driver.quit()


def pytest_configure(config):
    report_root = os.path.join(os.getcwd(), "reports")
    os.makedirs(report_root, exist_ok=True)
    config.report_root = report_root
    config.test_reports = {}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    test_file = item.fspath.basename.replace(".py", "")
    report_store = item.config.test_reports.setdefault(test_file, {})
    report_store[item.name] = report

    if report.failed:
        screenshot_dir = os.path.join(
            item.config.report_root,
            test_file
        )
        os.makedirs(screenshot_dir, exist_ok=True)

        if hasattr(item, "instance") and hasattr(item.instance, "driver"):
            screenshot_path = os.path.join(
                screenshot_dir,
                f"{item.name}_failure.png"
            )
            item.instance.driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")


def pytest_sessionfinish(session, exitstatus):

    if not hasattr(session.config, "test_reports"):
        return

    report_root = session.config.report_root

    for test_file, tests_dict in session.config.test_reports.items():

        report_dir = os.path.join(report_root, test_file)
        os.makedirs(report_dir, exist_ok=True)

        for test_name, report in tests_dict.items():

            report_path = os.path.join(
                report_dir,
                f"{test_name}.html"
            )

            status = (
                "PASSED"
                if report.passed
                else "FAILED"
                if report.failed
                else "SKIPPED"
            )

            color = (
                "#155724"
                if report.passed
                else "#721c24"
                if report.failed
                else "#856404"
            )

            background = (
                "#d4edda"
                if report.passed
                else "#f8d7da"
                if report.failed
                else "#fff3cd"
            )

            longrepr = ""
            if hasattr(report, "longrepr") and report.longrepr:
                longrepr = escape(str(report.longrepr))

            screenshot_file = os.path.join(
                report_dir,
                f"{test_name}_failure.png"
            )

            screenshot_html = ""

            if report.failed and os.path.exists(screenshot_file):
                image_name = os.path.basename(screenshot_file)

                screenshot_html = f"""
                <h2>Failure Screenshot</h2>
                <a href="{image_name}" target="_blank">
                    <img src="{image_name}"
                         alt="Failure Screenshot"
                         style="max-width:100%;border:1px solid #ccc;">
                </a>
                """

            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{escape(test_name)} - {status}</title>

<style>
body {{
    font-family: Arial, sans-serif;
    margin:20px;
}}

.banner {{
    padding:20px;
    border-radius:8px;
    background:{background};
    color:{color};
    margin-bottom:20px;
}}

pre {{
    background:#f8f9fa;
    border:1px solid #ddd;
    padding:15px;
    white-space:pre-wrap;
    word-wrap:break-word;
}}

img {{
    margin-top:15px;
    max-width:100%;
}}
</style>

</head>

<body>

<div class="banner">
<h1>{escape(test_name)}</h1>
<p><strong>Status:</strong> {status}</p>
<p><strong>Duration:</strong> {report.duration:.2f} sec</p>
</div>

<h2>Failure Details</h2>

<pre>{longrepr or "No failure details."}</pre>

{screenshot_html}

</body>

</html>
"""

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            print(f"Report generated: {report_path}")
