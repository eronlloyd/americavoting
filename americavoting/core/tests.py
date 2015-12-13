from django.test import TestCase
from django.db.utils import IntegrityError

from .models import Division


class DivisionTestCase(TestCase):
    def setUp(self):
        Division.objects.create(category="state", name="Pennsylvania",
                                abbreviation="pa", capital_city="Harrisburg",
                                data_source="Department of State",
                                slug="pennsylvania")

    def test_division_string_representation(self):
        """The division should properly represent itself as a string."""
        pa = Division.objects.get(name="Pennsylvania")
        self.assertEqual(str(pa), 'Pennsylvania')

    def test_division_abbreviation_length(self):
        ny = Division.objects.create()
        ny.abbreviation = "nys"
        ny.save()
        self.assertEqual(len(ny.abbreviation), 2)

    def test_duplicate_division_creation(self):
        """It shouldn't be possible to create duplicates of existing divisions."""
        self.assertRaisesMessage(IntegrityError, Division.objects.create,
                                 name="Pennsylvania")
