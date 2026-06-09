# core/conftest.py

from Common import *
from html import escape

# parallel-crossbrowser
# def pytest_addoption(parser):
#     parser.addoption("--mybrowser", action="store", default="chrome")
# @pytest.fixture(scope="class", params=["chrome", "firefox"])

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # parallel-crossbrowser
    # browser = request.config.getoption("--mybrowser")
    # if browser.lower() == "chrome":
    #     driver = webdriver.Chrome(
    #         service=ChromeService(ChromeDriverManager().install())
    #     )

    # elif browser.lower() == "firefox":
    #       driver = webdriver.Firefox(
    #         service=FirefoxService(GeckoDriverManager().install())
    #     )
    # else:
    #     raise Exception("Browser not supported")
    driver.maximize_window()
    driver.implicitly_wait(25)
    driver.get("https://stagedoctors.mediquince.com/")
    request.cls.driver = driver
    yield
    driver.quit()


def pytest_configure(config):
    config.test_reports = {}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture the test report and save failure screenshots per test file.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    test_file = item.fspath.basename.replace(".py", "")
    report_store = item.config.test_reports.setdefault(test_file, {})
    report_store[item.name] = report

    if report.failed:
        screenshot_dir = f"reports/{test_file}"
        os.makedirs(screenshot_dir, exist_ok=True)

        if hasattr(item, "instance") and hasattr(item.instance, "driver"):
            driver = item.instance.driver
            screenshot_path = f"{screenshot_dir}/{item.name}_failure.png"
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")


def pytest_sessionfinish(session, exitstatus):
    """
    Generate individual HTML reports for each test at the end of the session.
    """
    if not hasattr(session.config, "test_reports"):
        return

    for test_file, tests_dict in session.config.test_reports.items():
        report_dir = f"reports/{test_file}"
        os.makedirs(report_dir, exist_ok=True)

        for test_name, report in tests_dict.items():
            report_path = f"{report_dir}/{test_name}.html"
            status = "PASSED" if report.passed else "FAILED" if report.failed else "SKIPPED"
            color = "#155724" if report.passed else "#721c24" if report.failed else "#856404"
            background = "#d4edda" if report.passed else "#f8d7da" if report.failed else "#fff3cd"
            longrepr = ""
            if hasattr(report, "longrepr") and report.longrepr:
                longrepr = escape(str(report.longrepr))

            screenshot_file = f"{report_dir}/{test_name}_failure.png"
            screenshot_html = ""
            if report.failed and os.path.exists(screenshot_file):
                screenshot_html = (
                    f"<h2>Failure Screenshot</h2>"
                    f"<img src=\"{os.path.basename(screenshot_file)}\" alt=\"failure screenshot\" "
                    f"style=\"max-width:100%;border:1px solid #ccc;\"/>"
                )

            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{escape(test_name)} - {status}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .banner {{ padding: 20px; border-radius: 8px; background: {background}; color: {color}; margin-bottom: 20px; }}
        .banner h1 {{ margin: 0 0 10px; }}
        .details {{ margin-bottom: 20px; }}
        pre {{ background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }}
        img {{ display: block; margin-top: 10px; max-width: 100%; }}
    </style>
</head>
<body>
    <div class="banner">
        <h1>{escape(test_name)}</h1>
        <div>Status: <strong>{status}</strong></div>
        <div>Duration: {report.duration:.2f}s</div>
    </div>
    <div class="details">
        <h2>Test Output</h2>
        <pre>{longrepr or 'No failure details.'}</pre>
    </div>
    {screenshot_html}
</body>
</html>
"""

            with open(report_path, "w", encoding="utf-8") as html_file:
                html_file.write(html_content)

            print(f"Report generated: {report_path}")
