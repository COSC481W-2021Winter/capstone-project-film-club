from django.test import TestCase
from core.models import *
# Create your tests here.

class GenreTestCase(TestCase):
    def setUp(self):
        Genre.objects.create(name="CO", api_id=3)

    def test_genre_name(self):
        test = Genre.objects.get(api_id=3)
        self.assertEqual(test.__str__(), 'CO')