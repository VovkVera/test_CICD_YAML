from django.test import TestCase
from .models import Category

class CommercialTestCase(TestCase):

    def setUp(self):
        #c1 = Category.objects.create(group_name = "Books", description = "There are a lot of different books")
        c1 = Category.objects.create(group_name = "A", description = "aa")
        c1.save()


    def test_departures_count(self):
        c = Category.objects.get(group_name="A")
        #self.assertEqual(c.description, "There are a lot of different books")
        self.assertEqual(c.group_name, "A")
