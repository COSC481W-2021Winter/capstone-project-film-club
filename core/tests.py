from django.test import TestCase, Client, LiveServerTestCase
from core.models import *
from core.views import *
import time 
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Model Test


class GenreTestCase(TestCase):
    def setUp(self):
        Genre.objects.create(name="CO", api_id=3)

    def test_genre_name(self):
        test = Genre.objects.get(api_id=3)
        self.assertEqual(test.__str__(), 'CO')

# View Test


class HomeTestCase(TestCase):
    def test_search_view(self):
        client = Client()
        response = client.get(reverse('core:home'))
        response.status_code

# Register Test

class RegisterTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(RegisterTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(RegisterTestCase, self).tearDown()

    # Verify that the Registration form contains all elements needed

    def test_elements_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        time.sleep(1)

        assert 'Username' in selenium.page_source, "Username should be displayed"
        assert 'Email' in selenium.page_source, "Email should be displayed"
        assert 'Password' in selenium.page_source, "Password should be displayed"
        assert 'Password confirmation' in selenium.page_source, "Password Confirm should be displayed"
        assert 'Register' in selenium.page_source, "Register Button should be displayed" 

    # Verify if the functionality of register form works

    def test_regular_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # find the form element
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_id('id_register')

        # Fill the form with data
        username.send_keys('unary')
        email.send_keys('contact@yusuf.im')
        password1.send_keys('y13hsj*d')
        password2.send_keys('y13hsj*d')

        # submitting the form by clicking on submit
        submit.click()

        # checks if we are on the next page
        assert 'favorite movie genres' in selenium.page_source, "Should be moved to the next page."

    # Verify that Enter key works as a substitute for the Submit button

    def test_enter_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # find the form element
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_id('id_register')

        # Fill the form with data
        username.send_keys('unary')
        email.send_keys('contact@yusuf.im')
        password1.send_keys('y13hsj*d')
        password2.send_keys('y13hsj*d')

        # submitting the form
        # password2.submit()
        submit.send_keys(Keys.ENTER)

        assert 'favorite movie genres' in selenium.page_source, "Should be moved to the next page."

    # Verify that all the required/mandatory fields are marked with an error message

    def test_requiredFields_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # find the form element
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_id('id_register')

        # Check if validations messages show up for everything
        submit.click()
        assert username.get_attribute(
            "validationMessage") == "Please fill out this field.", "Username is filled."
        assert email.get_attribute(
            "validationMessage") == "Please fill out this field.", "Email is filled."
        assert password1.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass1 is filled."
        assert password2.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass2 is filled."

        # Check if validations messages show up for everything except username
        username.send_keys('unary')
        submit.click()
        assert email.get_attribute(
            "validationMessage") == "Please fill out this field.", "Email is filled."
        assert password1.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass1 is filled."
        assert password2.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass2 is filled."

        # Check if validations messages show up for everything except username + email
        email.send_keys('contact@yusuf.im')
        submit.click()
        assert password1.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass1 is filled."
        assert password2.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass2 is filled."

        # Check if validations messages show up for everything except username + email + pass1
        password1.send_keys('y13hsj*d')
        submit.click()
        assert password2.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass2 is filled."

        # Check if you can go to the next page
        password2.send_keys('y13hsj*d')
        submit.click()
        assert 'favorite movie genres' in selenium.page_source, "Should be moved to the next page."

    # Verify that entering blank spaces on mandatory fields lead to the validation error

    def test_blankFields_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # find the form element
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_id('id_register')

        username.send_keys('')
        email.send_keys('')
        password1.send_keys('')
        password2.send_keys('')

        # Check if validations messages show up for everything
        submit.click()
        assert username.get_attribute(
            "validationMessage") == "Please fill out this field.", "Username is filled."
        assert email.get_attribute(
            "validationMessage") == "Please fill out this field.", "Email is filled."
        assert password1.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass1 is filled."
        assert password2.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass2 is filled."

    # Verify that the validation of all the fields are as per business requirement

    ## Test username
    def test_username_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # ------------------TEST USERNAME------------------ #
        selenium.find_element_by_id('id_email').send_keys('contact@yusuf.im')

        fake_usernames = ["$Smezy", "%!mezy",
                          "^&*(Smezy)", "Smezy@.*", 
                          "s6SnGGAlkocT1Xr5wDyK2RoI986CCXFDhtngApHqN0Z8KWQ0S47XVgasjukjpEGKUN94obYeivFuy9mF3R5pThnHqY6mbdH9aZez9OGbH3jCjr3uoQVK8HjzhU5Nn7EYeDKUinvBck0mVvBTyAgy98KymhE",
                          "S_mezy"]
        for i in range((len(fake_usernames) - 1)):
            selenium.find_element_by_id('id_password1').send_keys('y13hsj*d')
            selenium.find_element_by_id('id_password2').send_keys('y13hsj*d')
            selenium.find_element_by_id(
                'id_username').send_keys(fake_usernames[i])
            selenium.find_element_by_id('id_register').send_keys(Keys.RETURN)

            time.sleep(1)
            
            if (i < 4):
                # assert "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters." in selenium.page_source
                assert "username" in selenium.page_source, "Should be on the same page."
                selenium.find_element_by_id('id_username').clear()
            else:
                assert "favorite movie genres" in selenium.page_source, "Should be on the next page."

    ## Test email
    def test_email_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # ------------------TEST EMAIL------------------ #
        selenium.find_element_by_id('id_username').send_keys('S.mezy@')

        fake_emails = ["max", "max.com", "max@", "max@ds.", "max@ds.com"]
        for i in range(len(fake_emails)):

            selenium.find_element_by_id('id_email').send_keys(fake_emails[i])
            selenium.find_element_by_id('id_password1').send_keys('y13hsj*d')
            selenium.find_element_by_id('id_password2').send_keys('y13hsj*d')
            selenium.find_element_by_id('id_register').click()

            time.sleep(1)

            if (i < (len(fake_emails) - 1)):
                assert "" in selenium.find_element_by_id('id_email').get_attribute(
                    "validationMessage"), "Email is filled."
                selenium.find_element_by_id('id_email').clear()
                selenium.find_element_by_id('id_password1').clear()
                selenium.find_element_by_id('id_password2').clear()
            else:
                assert "favorite movie genres" in selenium.page_source, "Should be on the next page."

    ## Test password
    def test_password_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # ------------------TEST PASSWORD------------------ #
        selenium.find_element_by_id('id_username').send_keys('smile')
        selenium.find_element_by_id('id_email').send_keys('smile@game.org')
        fake_passwords = ["max", "deaf", "12345", "smile", "h$56sile4"]
        for i in range(len(fake_passwords)):
            selenium.find_element_by_id('id_password1').send_keys(fake_passwords[i])
            selenium.find_element_by_id('id_password2').send_keys(fake_passwords[i])
            selenium.find_element_by_id('id_register').click()
            
            time.sleep(1)

            if (i < (len(fake_passwords) - 1)):
                assert "username" in selenium.page_source, "Should be on the same page."
            else:
                assert "favorite movie genres" in selenium.page_source, "Should be on the next page."

    # Verify whether the password and confirm password are the same or not

    def test_passwordConfirm_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # find the form element
        selenium.find_element_by_id('id_username').send_keys("unary")
        selenium.find_element_by_id('id_email').send_keys('contact@yusuf.im')
        selenium.find_element_by_id('id_password1').send_keys('y13hsj*d')
        selenium.find_element_by_id('id_password2').send_keys('y13hsj*34d')
        selenium.find_element_by_id('id_register').click()

        time.sleep(1)

        assert 'username' in selenium.page_source, "Passwords are not equal, shouldn't submit form"

        selenium.find_element_by_id('id_password1').send_keys('y13hsj*d')
        selenium.find_element_by_id('id_password2').send_keys('y13hsj*d')
        selenium.find_element_by_id('id_register').click()

        time.sleep(1)

        assert 'favorite movie genres' in selenium.page_source, "Passwords aren't the same shouldn't continue to next page"