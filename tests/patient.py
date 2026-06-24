from Common import *
from pages.login_page import Login
from pages.patient_page import Patient


@pytest.mark.usefixtures("setup")
class TestPatient:
    def test_login(self):
        Login(self.driver).do_login("7567546456", "789987")

    def test_patient_mod(self):
        Patient(self.driver).open_patient()

    def test_patient_create(self):
        patient = Patient(self.driver)
        patient.open_patient()
        patient.open_register_patient()

    def test_patient_details(self):
        patient = Patient(self.driver)
        patient.fill_patient_details(
            "8047020202",
            "Mr",
            "Bharathan",
            "01/02/1992",
            "55",
            "male",
            "Sivakasi",
        )
        patient.verify_patient_saved("Bharathan")






        


            
