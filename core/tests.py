from django.test import TestCase, Client, LiveServerTestCase
from core.models import *
from core.views import * 
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
# Create your tests here.

## Model Test
class GenreTestCase(TestCase):
    def setUp(self):
        Genre.objects.create(name="CO", api_id=3)

    def test_genre_name(self):
        test = Genre.objects.get(api_id=3)
        self.assertEqual(test.__str__(), 'CO')

## View Test
class HomeTestCase(TestCase):
    def test_search_view(self):
            client = Client()
            response = client.get(reverse('core:home'))
            response.status_code

#Templete Test
class GenresTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.signup()

    def tearDown(self):
        self.selenium.quit()
        super(GenresTestCase, self).tearDown()

    def signup(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/register')

        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')

        submit = selenium.find_element_by_class_name('btn')

        username.send_keys('Test123')
        email.send_keys('test123@test.com')
        password1.send_keys('homepagepass')
        password2.send_keys('homepagepass')

        submit.send_keys(Keys.RETURN)

        assert 'favorite movie genre' in selenium.page_source

    def test_pick_genres(self):
        selenium = self.selenium

        genre1 = Select(selenium.find_element_by_id('id_firstGenre'))
        genre2 = Select(selenium.find_element_by_id('id_secondGenre'))
        genre3 = Select(selenium.find_element_by_id('id_thirdGenre'))

        submit = selenium.find_element_by_class_name('btn')

        submit.send_keys(Keys.RETURN)
        
        Url = self.live_server_url + '/genre'

        self.assertNotEquals(self.live_server_url, Url)




from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from core.models import *
from core.views import *



import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager




## Model Test
class GenreTestCase(TestCase):
    def setUp(self):
        Genre.objects.create(name="CO", api_id=3)

    def test_genre_name(self):
        test = Genre.objects.get(api_id=3)
        self.assertEqual(test.__str__(), 'CO')

## View Test
class HomeTestCase(TestCase):
    def test_search_view(self):
            client = Client()
            response = client.get(reverse('core:home'))
            response.status_code

class HomePageTestCase(LiveServerTestCase):
	
	
	
	
	def setUp(self):
		self.selenium = webdriver.Chrome()
		self.signup()
		self.pick_genres()
		super(HomePageTestCase, self).setUp()

	def tearDown(self):
		self.selenium.quit()
		super(HomePageTestCase, self).tearDown()
		
	def signup(self):

		'''
		This is not a test even though the assert statement is tested.
		This is a segment of code that creates a new account.
		This is necessary for future tests.

		'''
		selenium = self.selenium
		selenium.get(self.live_server_url + '/register')
		username = selenium.find_element_by_id('id_username')
		email = selenium.find_element_by_id('id_email')
		password1 = selenium.find_element_by_id('id_password1')
		password2 = selenium.find_element_by_id('id_password2')
		
		
		submit = selenium.find_element_by_tag_name('button')
		
		username.send_keys('Test123')
		email.send_keys('test123@test.com')
		password1.send_keys('homepagepass')
		password2.send_keys('homepagepass')
		
		submit.send_keys(Keys.RETURN)
		
		assert 'favorite movie genre' in selenium.page_source
		
	def pick_genres(self):
		'''

		continues creation of account process

		'''
		selenium = self.selenium
		genre2 = Select(selenium.find_element_by_id('id_secondGenre'))
		genre3 = Select(selenium.find_element_by_id('id_thirdGenre'))
		
		
		submit = selenium.find_element_by_tag_name('button')
		
		
		submit.send_keys(Keys.RETURN)
		
	def test_loggingIN(self):
		selenium = self.selenium
		selenium.get(self.live_server_url + '/accounts/login')
		username = selenium.find_element_by_id('id_username')
		password = selenium.find_element_by_id('id_password')
		button = selenium.find_element_by_id('myBtn')
		assert '/accounts/password_reset/' in selenium.page_source
		assert 'login' in selenium.page_source 
		
	def test_home_success(self):
		selenium = self.selenium
		selenium.get(self.live_server_url + '/accounts/login')
		username = selenium.find_element_by_id('id_username')
		password = selenium.find_element_by_id('id_password')
		button = selenium.find_element_by_id('myBtn')
		username.send_keys('Test123')
		password.send_keys('homepagepass')
		button.send_keys(Keys.RETURN)
		selenium.get(self.live_server_url + '/Test123')
		
		#print(selenium.page_source)
		assert 'Home' in selenium.page_source

		#time.sleep(15)

	def test_home_failure(self):
		selenium = self.selenium
		selenium.get(self.live_server_url + '/accounts/login')
		username = selenium.find_element_by_id('id_username')
		password = selenium.find_element_by_id('id_password')
		button = selenium.find_element_by_id('myBtn')
		username.send_keys('asch')
		password.send_keys('Sha')
		button.send_keys(Keys.RETURN)
		selenium.get(self.live_server_url + '/asch')
		
		assert '500' in selenium.page_source

	

	def test_resetBasic(self):
		selenium = self.selenium

		selenium.get(self.live_server_url + '/accounts/password_reset')
		EMAIL = selenium.find_element_by_id('id_email')
		submit = selenium.find_element_by_xpath("//input[@type='submit']")
		submit.send_keys(Keys.RETURN)
		assert 'Forgotten your password? Enter your email address below, and we’ll email instructions for setting a new one.' in selenium.page_source

	def test_resetBasic_no_sym(self):
		selenium = self.selenium

		selenium.get(self.live_server_url + '/accounts/password_reset')
		EMAIL = selenium.find_element_by_id('id_email')
		submit = selenium.find_element_by_xpath("//input[@type='submit']")
		EMAIL.send_keys('asch')
		submit.send_keys(Keys.RETURN)
		assert 'Forgotten your password? Enter your email address below, and we’ll email instructions for setting a new one.' in selenium.page_source

	def test_resetBasic_notemail_valid(self):
		selenium = self.selenium

		selenium.get(self.live_server_url + '/accounts/password_reset')
		EMAIL = selenium.find_element_by_id('id_email')
		submit = selenium.find_element_by_xpath("//input[@type='submit']")
		EMAIL.send_keys('asch@wwwwwwww')
		submit.send_keys(Keys.RETURN)
		assert 'Enter a valid email address.' in selenium.page_source

	def test_resetBasic_notemail_valid(self):
		selenium = self.selenium

		selenium.get(self.live_server_url + '/accounts/password_reset')
		EMAIL = selenium.find_element_by_id('id_email')
		submit = selenium.find_element_by_xpath("//input[@type='submit']")
		EMAIL.send_keys('asch@wwwwwwww')
		submit.send_keys(Keys.RETURN)
		assert 'Enter a valid email address.' in selenium.page_source

	def test_resetBasic_email_valid(self):
		selenium = self.selenium

		selenium.get(self.live_server_url + '/accounts/password_reset')
		EMAIL = selenium.find_element_by_id('id_email')
		submit = selenium.find_element_by_xpath("//input[@type='submit']")
		EMAIL.send_keys('test123@test.com')
		submit.send_keys(Keys.RETURN)
		assert 'We’ve emailed you instructions for setting your password,' in selenium.page_source

	





