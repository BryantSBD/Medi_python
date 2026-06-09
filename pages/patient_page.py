from Common import *

class Patient:
    def __init__(self, driver):
        self.driver = driver

    def open_patient(self):
        wait = WebDriverWait(self.driver, 25)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "site-preloader")))
        self.driver.find_element(By.CSS_SELECTOR, "a[href*='customers']").click()
        title = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".page-title"))
        ).text
        assert "Patients" in title, "Patient page did not open"

    def open_register_patient(self):
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-danger.action-btn.dropdown-toggle").click()
        self.driver.find_element(By.ID, "qk_RegPat").click()

    def fill_patient_details(self, phone, title,first_name, dob, age, gender, city):
        self.driver.find_element(By.ID, "phone_no").send_keys(phone)
        self.driver.find_element(By.ID, "select2-usr_prefix-container").click()
        self.driver.find_element(By.CLASS_NAME, "select2-search__field").send_keys(title)
        self.driver.find_element(By.XPATH, "/html/body/span/span/span[2]/ul/li[1]").click()
        self.driver.find_element(By.ID, "first_name").send_keys(first_name)
        self.driver.find_element(By.ID, "date_of_birth").send_keys(dob)
        self.driver.find_element(By.ID, "chng_ageswitch").click()
        self.driver.find_element(By.ID, "age").send_keys(age)
        self.driver.find_element(By.ID, "select2-pat_gen-container").click()
        self.driver.find_element(By.CLASS_NAME, "select2-search__field").send_keys(gender)
        self.driver.find_element(By.XPATH, "/html/body/span/span/span[2]/ul/li[1]").click()
        self.driver.find_element(By.ID, "city_txt").send_keys(city)
        self.driver.find_element(By.CLASS_NAME, "skpPatVrfyPopup").click()
        self.driver.find_element(By.ID, "saveapp").click()

    def verify_patient_saved(self, expected_name):
        self.driver.find_element(By.ID, "otp_code").send_keys("123456")
        self.driver.find_element(By.ID, "verfiy_otp").click()
        wait = WebDriverWait(self.driver, 25)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "site-preloader")))
        element = self.driver.find_element(By.XPATH, "/html/body/div[8]/div[1]/div[5]/div/div/div/div/div/div[3]/div[4]/div/div/table[1]/tbody/tr[1]/td[3]/div[1]/div")
        assert element.text == expected_name, "That patient name not in the list"
        report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "Patient")
        os.makedirs(report_dir, exist_ok=True)
        self.driver.save_screenshot(os.path.join(report_dir, "patient.jpg"))