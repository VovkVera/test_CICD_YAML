from django.test import TestCase
from .models import Category
class FlightTestCase(TestCase):

    def setUp(self):
        c1 = Category.objects.create(group_name = "Books", description = "There are a lot of different books")
        c1.save()


    def test_departures_count(self):
        c = Category.objects.get(group_name="Books")
        self.assertEqual(c.description, "There are a lot of different books")
