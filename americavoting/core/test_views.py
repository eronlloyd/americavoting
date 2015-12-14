from django.test import TestCase
from django.http import HttpRequest, HttpResponse

from .models import Division
from .views import division_index, division_detail


class DivisionIndexTestCase(TestCase):

    def setUp(self):
        Division.objects.create(name="Pennsylvania")

    def test_query_set_includes_existing_objects(self):
        """Test that query returns any existing Division objects."""
        request = HttpRequest()
        response = division_index(request)
        test_qs = Division.objects.all()
        self.assertIn('Pensylvania', response.content.decode())

    def test_query_set_excludes_non_existing_objects(self):
        """Test that query doesn't return any non-existant Division objects."""
        request = HttpRequest()
        response = division_index(request)
        test_qs = Division.objects.all()
        self.assertNotIn('Mariland', response.content.decode())


class DivisionDetailTestCase(TestCase):

    def setUp(self):
        Division.objects.create(name="Pennsylvania", slug='pennsylvania')

    def test_lookup(self):
        request = HttpRequest()
        response = division_detail(request, 'pennsylvania')
        self.assertIn('Pennsylvania', response.content.decode())
