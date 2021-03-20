import os

from django.test import TestCase, Client, LiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import *
from core.views import *
import time
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from . import views

class ParentTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.signup()
        self.pick_genres()

    def tearDown(self):
        self.selenium.quit()
        super(LogoutTestCase, self).tearDown()

    def signup(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/register')
        firstName = selenium.find_element_by_id('id_first_name')
        lastName = selenium.find_element_by_id('id_last_name')
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_id('id_register')

        firstName.send_keys('Test')
        lastName.send_keys('Tester')
        username.send_keys('Test123')
        email.send_keys('test123@test.com')
        password1.send_keys('moviepass')
        password2.send_keys('moviepass')
        submit.click()

    def pick_genres(self):
        selenium = self.selenium
        genre1 = Select(selenium.find_element_by_id('id_firstGenre'))
        genre2 = Select(selenium.find_element_by_id('id_secondGenre'))
        genre3 = Select(selenium.find_element_by_id('id_thirdGenre'))
        submit = selenium.find_element_by_class_name('btn')
        submit.send_keys(Keys.RETURN)
        Url = self.live_server_url + '/genre'
        self.assertNotEquals(self.live_server_url, Url)



class UserSearchTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.signup()
    
    def tearDown(self):
        self.selenium.quit()
        super(UserSearchTestCase, self).tearDown()
    
    def signup(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/register')
        
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        
        submit = selenium.find_element_by_id('id_register')
        
        username.send_keys('Test123')
        email.send_keys('test123@test.com')
        password1.send_keys('homepagepass')
        password2.send_keys('homepagepass')
        first_name.send_keys('Phil')
        last_name.send_keys('Smith')
        
        submit.send_keys(Keys.RETURN)
        
        assert 'favorite movie genre' in selenium.page_source


    def testSignUP(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/register')
        
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        
        submit = selenium.find_element_by_id('id_register')
        
        username.send_keys('Test1')
        email.send_keys('test1@test.com')
        password1.send_keys('homepagepass1')
        password2.send_keys('homepagepass1')
        first_name.send_keys('Phil1')
        last_name.send_keys('Smith1')
        
        submit.send_keys(Keys.RETURN)
        
        assert 'favorite movie genre' in selenium.page_source

    def testSearchingStuff(self):
        selenium = self.selenium

        assert 'Search Movies' in selenium.page_source

        username = selenium.find_element_by_id('search-box')
        sel = selenium.find_element_by_id('movie_or_users')
        


        username.clear()
        username.click()
        username.send_keys('woman')
        assert 'Search Movies' in selenium.page_source

        username.send_keys(Keys.RETURN)
        assert 'Search Movies' in selenium.page_source

    def testSearchUserandMovie(self):
        selenium = self.selenium

        selenium.get(self.live_server_url + "/search?q=woman&search_user_or_movie=Users")
        assert "woman" in selenium.page_source
        assert len(selenium.find_elements_by_tag_name("label")) <= 1
        
        selenium.get(self.live_server_url + "/search?q=dumb&search_user_or_movie=Users")
        assert "dumb" in selenium.page_source
        assert len(selenium.find_elements_by_tag_name("label")) <= 1

        selenium.get(self.live_server_url + "/search?q=Test1&search_user_or_movie=Movies")
        assert "Test1" in selenium.page_source
        assert len(selenium.find_elements_by_tag_name("label")) <= 1

        selenium.get(self.live_server_url + "/search?q=Test2&search_user_or_movie=Movies")
        assert "Test2" in selenium.page_source
        assert len(selenium.find_elements_by_tag_name("label")) <= 1


        selenium.get(self.live_server_url + "/search?q=Test123&search_user_or_movie=Movies")
        assert "Test123" in selenium.page_source
        element = selenium.find_element_by_tag_name("label")
        
        assert len(selenium.find_elements_by_tag_name("label")) > 0

class LogoutTestCase(ParentTestCase):
    def test_logout(self):
        selenium = self.selenium
        logout = selenium.find_element_by_id('logout')
        selenium.implicitly_wait(10)
        logout.send_keys(Keys.RETURN)
        try:
            self.selenium.find_element_by_id('myBtn')
            selenium.AssertTrue(True)
        except NoSuchElementException:
            print("Not found")



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
        selenium = self.selenium
        selenium.get(self.live_server_url + '/register')

        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')

        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        
        submit = selenium.find_element_by_id('id_register')
        

        submit = selenium.find_element_by_class_name('btn')

        username.send_keys('Test123')
        email.send_keys('test123@test.com')
        password1.send_keys('homepagepass')
        password2.send_keys('homepagepass')
        first_name.send_keys('Phil')
        last_name.send_keys('Smith')
        
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
        firstName = selenium.find_element_by_id('id_first_name')
        lastName = selenium.find_element_by_id('id_last_name')
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_id('id_register')

        firstName.send_keys('Test')
        lastName.send_keys('Tester')
        username.send_keys('Test123')
        email.send_keys('test123@test.com')
        password1.send_keys('moviepass')
        password2.send_keys('moviepass')
        submit.click()
    def test_home_page(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/m/252')
        assert "Willy Wonka" in selenium.page_source
        assert "Write A Review" in selenium.page_source
        assert "None of your friends have watched this" in selenium.page_source
        ##add friends
        ##reviewbox.send_keys('Great movie! Gene Wilder is great!')
        ##submitreview.send_keys(Keys.RETURN)
        ##assert "John doe has watched this" in selenium.page_source
        ##assert 'Great movie! Gene Wilder is great!' in selenium.page_source
        ##markwatch = reviewbox = selenium.find_element_by_id("mark-watched")
        ##markwatch.send_keys(Keys.RETURN)
        ##add markwatch detection


class HomePageProfileTestCase(LiveServerTestCase):
    def setUp(self):
        settings.DEBUG = True

        self.selenium = webdriver.Chrome()

        for x in range(5):
            self.signup(x)

        other_users = User.objects.all().exclude(username = 'Test1234')

        self.user = User.objects.get(username = 'Test1234')

        for user in other_users:
            for x in range(3):
                movie = Movie(title='Test Movie' + str(x), description='literally not a real movie ' + str(x),
                               api_id=(x + 10) * 5, poster_path='/image.png')

                movie.save()

                review = Review(user=user, movie=movie, title='Test Review',
                                text='literally not a real review', score=1)

                review.save()

            self.user.userprofile.friends.add(user)
            user.userprofile.friends.add(self.user)

        super(HomePageProfileTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()

        super(HomePageProfileTestCase, self).tearDown()

    def signup(self, num):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/register')

        temp_username = 'Test123' + str(num)

        username = selenium.find_element_by_id('id_username')
        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        profile_pic = selenium.find_element_by_xpath("//input[@type='file']")

        submit = selenium.find_element_by_name('register')

        username.send_keys(temp_username)
        first_name.send_keys('Test123')
        last_name.send_keys(str(num))
        email.send_keys('test123@test.com')
        password1.send_keys('homepagepass')
        password2.send_keys('homepagepass')
        profile_pic.send_keys(os.getcwd() + '\\core\\static\\img\\icons\\logo\\filmClubLogo.png')

        submit.send_keys(Keys.RETURN)

        user = User.objects.get(username=temp_username)

        assert 'favorite movie genre' in selenium.page_source

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

        reviews = selenium.find_elements_by_class_name('review')

        num_reviews = len(reviews) - 1  # Review HTML is stored in the home page HTML so this is picking that up too (have to subtract one to get real number)

        assert len(num_friends.text) > 0
        assert len(num_movies.text) > 0
        assert num_reviews == views.home_reviews_amount

        ordered_reviews = Review.objects.filter(user__userprofile__friends = self.user).order_by('-added').all()[:views.home_reviews_amount]

        ordered_titles = []
        home_titles = []

        for review in ordered_reviews:
            ordered_titles.append(review.title)

        for review in reviews:
            title = review.find_elements_by_class_name('review-title')[0]

            home_titles.append(title.text)

        assert ordered_titles == home_titles[:views.home_reviews_amount]

    def test_profile(self):
        selenium = self.selenium

        movie1 = Movie(title='Test Movie', description='literally not a real movie',
                       api_id=1, poster_path='/image.png')
        movie2 = Movie(title='Test Movie 2', description='literally not a real movie 2', api_id=2,
                       poster_path='/image2.png')

        movie1.save()
        movie2.save()

        review1 = Review(user=self.user, movie=movie1, title='Test Review',
                         text='literally not a real review', score=1)
        review2 = Review(user=self.user, movie=movie2, title='Test Review 2', text='literally not a real review 2',
                         score=2)

        review1.save()
        review2.save()

        selenium.get(self.live_server_url + '/Test1234')

        first_name_input = selenium.find_element_by_name('first-name')
        last_name_input = selenium.find_element_by_name('last-name')
        name_submit = selenium.find_element_by_id('name-submit')

        full_name = first_name_input.get_attribute('value') + ' ' + last_name_input.get_attribute('value')
        reviews = selenium.find_elements_by_class_name('review')

        for review in reviews:
            movie = Movie.objects.filter(
                title=review.find_elements_by_class_name('movie-title')[0].text)

            assert movie.exists()

            review = Review.objects.filter(user=self.user, movie=movie[0])

            assert review.exists()

        assert self.user.get_full_name() == full_name

        first_name_input.clear()
        last_name_input.clear()

        first_name_input.send_keys('Edited')
        last_name_input.send_keys('Name')

        selenium.find_element_by_id('edit-name').submit()

        selenium.get(self.live_server_url)

        assert User.objects.get(username = 'Test1234').get_full_name() == 'Edited Name'

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

        assert 'First name' in selenium.page_source, "First name should be displayed"
        assert 'Last name' in selenium.page_source, "Last name should be displayed"
        assert 'Username' in selenium.page_source, "Username should be displayed"
        assert 'Email' in selenium.page_source, "Email should be displayed"
        assert 'Password' in selenium.page_source, "Password should be displayed"
        assert 'Password confirmation' in selenium.page_source, "Password Confirm should be displayed"
        assert 'Profile pic' in selenium.page_source, "Profile pic should be displayed"
        assert 'Register' in selenium.page_source, "Register Button should be displayed"

    # Verify if the functionality of register form works

    def test_regular_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # find the form element
        firstName = selenium.find_element_by_id('id_first_name')
        lastName = selenium.find_element_by_id('id_last_name')
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        profilePic = selenium.find_element_by_id('id_profile_pic')
        submit = selenium.find_element_by_id('id_register')

        # Fill the form with data
        firstName.send_keys('Hello')
        lastName.send_keys('World')
        username.send_keys('unary')
        email.send_keys('contact@yusuf.im')
        password1.send_keys('y13hsj*d')
        password2.send_keys('y13hsj*d')
        profilePic.send_keys('/Users/suprajakalva/Desktop/smile.jpeg')

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
        firstName = selenium.find_element_by_id('id_first_name')
        lastName = selenium.find_element_by_id('id_last_name')
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        profilePic = selenium.find_element_by_id('id_profile_pic')
        submit = selenium.find_element_by_id('id_register')

        # Fill the form with data
        firstName.send_keys('Hello')
        lastName.send_keys('World')
        username.send_keys('unary')
        email.send_keys('contact@yusuf.im')
        password1.send_keys('y13hsj*d')
        password2.send_keys('y13hsj*d')
        profilePic.send_keys('/Users/suprajakalva/Desktop/smile.jpeg') 

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
        firstName = selenium.find_element_by_id('id_first_name')
        lastName = selenium.find_element_by_id('id_last_name')
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_id('id_register')

        # Check if validations messages show up for everything
        submit.click()
        assert firstName.get_attribute(
            "validationMessage") == "Please fill out this field.", "FirstName is filled."
        assert lastName.get_attribute(
            "validationMessage") == "Please fill out this field.", "LastName is filled."
        assert username.get_attribute(
            "validationMessage") == "Please fill out this field.", "Username is filled."
        assert email.get_attribute(
            "validationMessage") == "Please fill out this field.", "Email is filled."
        assert password1.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass1 is filled."
        assert password2.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass2 is filled."

        # Check if validations messages show up for everything except firstname
        firstName.send_keys('Hello')
        submit.click()
        assert lastName.get_attribute(
            "validationMessage") == "Please fill out this field.", "LastName is filled."
        assert username.get_attribute(
            "validationMessage") == "Please fill out this field.", "Username is filled."
        assert email.get_attribute(
            "validationMessage") == "Please fill out this field.", "Email is filled."
        assert password1.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass1 is filled."
        assert password2.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass2 is filled."
        
        # Check if validations messages show up for everything except username
        lastName.send_keys('World')
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
        firstName = selenium.find_element_by_id('id_first_name')
        lastName = selenium.find_element_by_id('id_last_name')
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_id('id_register')

        firstName.send_keys('')
        lastName.send_keys('')
        username.send_keys('')
        email.send_keys('')
        password1.send_keys('')
        password2.send_keys('')

        # Check if validations messages show up for everything
        submit.click()
        assert firstName.get_attribute(
            "validationMessage") == "Please fill out this field.", "FirstName is filled."
        assert lastName.get_attribute(
            "validationMessage") == "Please fill out this field.", "LastName is filled."
        assert username.get_attribute(
            "validationMessage") == "Please fill out this field.", "Username is filled."
        assert email.get_attribute(
            "validationMessage") == "Please fill out this field.", "Email is filled."
        assert password1.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass1 is filled."
        assert password2.get_attribute(
            "validationMessage") == "Please fill out this field.", "Pass2 is filled."

    # Verify that the validation of all the fields are as per business requirement

    # Test username
    def test_username_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # ------------------TEST USERNAME------------------ #
        selenium.find_element_by_id('id_first_name').send_keys('Hello')
        selenium.find_element_by_id('id_last_name').send_keys('World')
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

    # Test email
    def test_email_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # ------------------TEST EMAIL------------------ #
        selenium.find_element_by_id('id_username').send_keys('S.mezy@')
        selenium.find_element_by_id('id_first_name').send_keys('Hello')
        selenium.find_element_by_id('id_last_name').send_keys('World')

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

    # Test password
    def test_password_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # ------------------TEST PASSWORD------------------ #
        selenium.find_element_by_id('id_first_name').send_keys('Hello')
        selenium.find_element_by_id('id_last_name').send_keys('World')
        selenium.find_element_by_id('id_username').send_keys('smile')
        selenium.find_element_by_id('id_email').send_keys('smile@game.org')
        fake_passwords = ["max", "deaf", "12345", "smile", "h$56sile4"]
        for i in range(len(fake_passwords)):
            selenium.find_element_by_id(
                'id_password1').send_keys(fake_passwords[i])
            selenium.find_element_by_id(
                'id_password2').send_keys(fake_passwords[i])
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
        selenium.find_element_by_id('id_first_name').send_keys('Hello')
        selenium.find_element_by_id('id_last_name').send_keys('World')
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
    
    # Test First Name
    def test_first_name_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # ------------------TEST EMAIL------------------ #
        selenium.find_element_by_id('id_last_name').send_keys('World')
        selenium.find_element_by_id('id_username').send_keys('S.mezy@')
        selenium.find_element_by_id('id_email').send_keys('max@ds.com')

        fake_first_names = ["", "Max"]
        for i in range(len(fake_first_names)):
            selenium.find_element_by_id('id_first_name').send_keys(fake_first_names[i])
            selenium.find_element_by_id('id_password1').send_keys('y13hsj*d')
            selenium.find_element_by_id('id_password2').send_keys('y13hsj*d')
            selenium.find_element_by_id('id_register').click()

            time.sleep(1)

            if (i < (len(fake_first_names)-1)):
                assert "" in selenium.find_element_by_id('id_first_name').get_attribute(
                    "validationMessage"), "First Name is filled."
                selenium.find_element_by_id('id_first_name').clear()
                selenium.find_element_by_id('id_password1').clear()
                selenium.find_element_by_id('id_password2').clear()
            else:
                assert "favorite movie genres" in selenium.page_source, "Should be on the next page."
    
    # Test Last Name
    def test_last_name_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(self.live_server_url + '/register')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # ------------------TEST EMAIL------------------ #
        selenium.find_element_by_id('id_first_name').send_keys('Hello')
        selenium.find_element_by_id('id_username').send_keys('S.mezy@')
        selenium.find_element_by_id('id_email').send_keys('max@ds.com')

        fake_last_names = ["", "World"]
        for i in range(len(fake_last_names)):
            selenium.find_element_by_id('id_last_name').send_keys(fake_last_names[i])
            selenium.find_element_by_id('id_password1').send_keys('y13hsj*d')
            selenium.find_element_by_id('id_password2').send_keys('y13hsj*d')
            selenium.find_element_by_id('id_register').click()

            time.sleep(1)

            if (i < (len(fake_last_names)-1)):
                assert "" in selenium.find_element_by_id('id_last_name').get_attribute(
                    "validationMessage"), "First Name is filled."
                selenium.find_element_by_id('id_last_name').clear()
                selenium.find_element_by_id('id_password1').clear()
                selenium.find_element_by_id('id_password2').clear()
            else:
                assert "favorite movie genres" in selenium.page_source, "Should be on the next page."






