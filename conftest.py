# core/conftest.py

from Common import *
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