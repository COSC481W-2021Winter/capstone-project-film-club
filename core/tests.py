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

#Search Results Page Test
class SearchPageTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(SearchPageTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SearchPageTestCase, self).tearDown()

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

    def enterSearch(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/genres')

        queryTerm = selenium.find_element_by_id('search-box')
        searchQuery = selenium.find_element_by_id('search-box')

        queryTerm.send_keys('Captain Marvel')

        searchQuery.send_keys(Keys.RETURN)

        Url = self.live_server_url + '/search'

        self.assertNotEquals(self.live_server_url, Url)


    def testResults(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/search?q=captain+marvel')

        if selenium.find_elements_by_css_selector('#search-results > a:nth-child(1) > div > div.movie-poster > img'):
            print("Movie Poster exists")
        if selenium.find_elements_by_css_selector('#search-results > a:nth-child(1) > div > div.movie-details > p.movie-title'):
            print("Movie Title exists")
        if selenium.find_elements_by_css_selector('#search-results > a:nth-child(1) > div > div.movie-details > p.movie-description'):
            print("Movie Description exists")

        assert "Captain Marvel" in selenium.page_source

        clickMovie = selenium.find_element_by_id('search-movie')

        clickMovie.send_keys(Keys.RETURN)

        Url = self.live_server_url + '/movie'

        self.assertNotEquals(self.live_server_url, Url)


