from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

# URL of the application (adjust accordingly)
url = 'http://127.0.0.1:8000/api/auth/login_view/'
driver.get(url)

# Test case for creating a patient
def test_creer_dpi():
    try:
        # 1. Log in as a user with the role 'PA'
        login_user = 'boyd123'
        login_password = 'password112'
        
        # Locate login fields and submit credentials
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_field.send_keys(login_user)
        password_field.send_keys(login_password)
        login_button.click()

        # Wait for login to complete (adjust if necessary)
        time.sleep(3)

        # 2. Navigate to the "Create Patient" page (adjust URL accordingly)
        create_patient_url = 'http://127.0.0.1:8000/api/personnel/creer_DPI/'
        driver.get(create_patient_url)
        
        # 3. Fill in the patient creation form
        user_data = {
            'username': 'new_user',
            'password': 'new_user_password',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com'
        }
        patient_data = {
            'numero_securite_sociale': '1234567890123',
            'date_naissance': '1985-07-10',
            'telephone': '0123456789',
            'adresse': '1234 Main St',
            'medecin_traitant': 'Dr. Smith',
            'personne_contact_nom': 'Jane Doe',
            'personne_contact_telephone': '0987654321'
        }
        dossier_data = {
            'antecedents': 'Aucune'
        }

        # Fill in the user data
        for field, value in user_data.items():
            driver.find_element(By.NAME, field).send_keys(value)
        
        # Fill in the patient data
        for field, value in patient_data.items():
            driver.find_element(By.NAME, field).send_keys(value)

        # Fill in dossier data
        driver.find_element(By.NAME, 'antecedents').send_keys(dossier_data['antecedents'])

        # 4. Submit the form
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()

        # 5. Wait for the response and verify successful creation
        time.sleep(3)

        error_message = driver.find_element(By.XPATH, '//div[contains(text(), "Accès non autorisé")]')
        assert error_message is not None, "Error message 'Accès non autorisé' was not found"

        # Check for success message or error
        success_message = driver.find_element(By.XPATH, '//div[contains(text(), "Patient et dossier créés avec succès")]')
        assert success_message is not None, "Patient creation failed"

        # Optionally, check if the new user, patient, and dossier appear in the response
        user_name = driver.find_element(By.XPATH, '//div[@id="user-details"]').text
        assert 'new_user' in user_name, "User not created properly"
        
        print("Test passed!")

    except Exception as e:
        print(f"Test failed: {str(e)}")

    finally:
        driver.quit()

# Run the test
test_creer_dpi()
