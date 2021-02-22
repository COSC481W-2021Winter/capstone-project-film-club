from django.test import TestCase, Client
from core.models import *
from core.views import * 
from django.urls import reverse
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