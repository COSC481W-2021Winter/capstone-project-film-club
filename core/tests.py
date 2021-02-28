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
class MoviePageTest(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()

        self.signup()

        super(MoviePageTest, self).setUp()

    def tearDown(self):

        self.selenium.quit()

        super(MoviePageTest, self).tearDown()
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
        password1.send_keys('moviepass')
        password2.send_keys('moviepass')

        submit.send_keys(Keys.RETURN)

        assert 'favorite movie genre' in selenium.page_source
    def test_home_page(self):

        selenium = self.selenium
        selenium.get(self.live_server_url +'/m/252')
        reviewbox = selenium.find_element_by_name("text")
        submitreview = selenium.find_element_by_name("Post")
        
        assert "Willy Wonka" in selenium.page_source
        assert "Write A Review" in selenium.page_source

        reviewbox.send_keys('Great movie! Gene Wilder is great!')
        submitreview.send_keys(Keys.RETURN)

        assert 'Great movie! Gene Wilder is great!' in selenium.page_source
        markwatch = reviewbox = selenium.find_element_by_id("mark-watched")
        markwatch.send_keys(Keys.RETURN)
        ##add markwatch detection
