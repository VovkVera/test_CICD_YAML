from django.db.models import Max
from django.test import TestCase

from .models import Category

class CommercialTestCase(TestCase):

    def setUp(self):

        c1 = Category.objects.create(group_name = "A", description = "There are a lot of different books")
        c1.save()

    def test_description(self):
        c = Category.objects.get(group_name="A")
        self.assertEqual(c.description, "There are a lot of different books?")

        

