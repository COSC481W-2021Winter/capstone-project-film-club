from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from core.models import *
from core.views import *

from django.test import TestCase, Client, LiveServerTestCase
from core.models import *
from core.views import *
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


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


# Templete Test
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
        selenium.get(self.live_server_url + '/m/252')
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


class HomePageProfileTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()

        self.signup()
        self.pick_genres()

        super(HomePageProfileTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()

        super(HomePageProfileTestCase, self).tearDown()

    def signup(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/register')

        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')

        submit = selenium.find_element_by_name('register')

        username.send_keys('Test123')
        email.send_keys('test123@test.com')
        password1.send_keys('homepagepass')
        password2.send_keys('homepagepass')

        submit.send_keys(Keys.RETURN)

        self.user = User.objects.get(username='Test123')

        assert 'favorite movie genre' in selenium.page_source

    def pick_genres(self):
        selenium = self.selenium

        genre2 = Select(selenium.find_element_by_id('id_secondGenre'))
        genre3 = Select(selenium.find_element_by_id('id_thirdGenre'))

        submit = selenium.find_element_by_name('submit')

        # genre2.select_by_index(2)
        # genre3.select_by_index(3)

        submit.send_keys(Keys.RETURN)

        # print(selenium.page_source)

        # assert 'Daily Recommendations' in selenium.page_source

    def test_home_page(self):
        selenium = self.selenium
        selenium.get(self.live_server_url)

        num_friends = selenium.find_element_by_id('num-friends')
        num_movies = selenium.find_element_by_id('num-movies')
        recently_watched = selenium.find_elements_by_class_name('rec-movie')

        if len(recently_watched) == 0:
            try:
                no_recent = selenium.find_element_by_id('no-recent')
            except:
                assert len(recently_watched) > 0

        assert len(num_friends.text) > 0
        assert len(num_movies.text) > 0

    def test_profile(self):
        selenium = self.selenium

        movie1 = Movie(title='Test Movie', description='literally not a real movie', api_id=1, poster_path='/image.png')
        movie2 = Movie(title='Test Movie 2', description='literally not a real movie 2', api_id=2,
                       poster_path='/image2.png')

        movie1.save()
        movie2.save()

        review1 = Review(user=self.user, movie=movie1, title='Test Review', text='literally not a real review', score=1)
        review2 = Review(user=self.user, movie=movie2, title='Test Review 2', text='literally not a real review 2',
                         score=2)

        review1.save()
        review2.save()

        selenium.get(self.live_server_url + '/Test123')

        full_name = selenium.find_element_by_id('user-full-name').text
        reviews = selenium.find_elements_by_class_name('review')

        for review in reviews:
            movie = Movie.objects.filter(title=review.find_elements_by_class_name('media-title')[0].text)

            assert movie.exists()

            review = Review.objects.filter(user=self.user, movie=movie[0])

            assert review.exists()

        assert self.user.get_full_name() == full_name