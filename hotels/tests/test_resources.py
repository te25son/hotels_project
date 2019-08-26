import tablib

from django.test import TestCase

from ..resources import CityResource, HotelResource
from ..models import City, Hotel


class CityResourceTests(TestCase):

    def setUp(self):
        self.resource = CityResource()
        self.dataset = tablib.Dataset(
            headers=['test-abbrv', 'test-name']
        )

    def test_fields(self):
        fields = self.resource.fields
        self.assertIn('abbrv', fields)
        self.assertIn('name', fields)

    def test_excluded_fields(self):
        fields = self.resource.fields
        self.assertNotIn('id', fields)

    def test_before_import(self):
        self.resource.before_import(
            self.dataset
        )
        self.assertEquals(self.dataset.headers, ['abbrv', 'name'])
        self.assertEquals(self.dataset.height, 1)  # Original headers should have been appended to the dataset making the height one not including the new headers
        self.assertEquals(self.dataset['abbrv'], ['test-abbrv'])
        self.assertEquals(self.dataset['name'], ['test-name'])

    def test_import_data(self):
        imported_data = self.resource.import_data(
            self.dataset,
            raise_errors=True
        )
        self.assertFalse(imported_data.has_errors())
        self.assertEquals(len(imported_data.rows), 1)

        imported_object = City.objects.get(name='test-name')
        self.assertEquals(imported_object.abbrv, 'test-abbrv')


class HotelResourceTests(TestCase):

    def setUp(self):
        self.resource = HotelResource()
        self.dataset = tablib.Dataset(
            headers=['test-city-abbrv', 'test-loc', 'test-name']
        )

    def test_fields(self):
        fields = self.resource.fields
        self.assertIn('city', fields)
        self.assertIn('loc', fields)
        self.assertIn('name', fields)

    def test_excluded_fields(self):
        fields = self.resource.fields
        self.assertNotIn('id', fields)

    def test_before_import(self):
        self.resource.before_import(
            self.dataset
        )
        self.assertEquals(self.dataset.headers, ['city', 'loc', 'name'])
        # Original headers should have been appended to the dataset making the height one not including the new headers
        self.assertEquals(self.dataset.height, 1)
        self.assertEquals(self.dataset['city'], ['test-city-abbrv'])
        self.assertEquals(self.dataset['loc'], ['test-loc'])
        self.assertEquals(self.dataset['name'], ['test-name'])

    def test_import_data(self):
        # City object must be imported before foreignkey can be paired
        city = City.objects.create(abbrv='test-city-abbrv', name='test-city-name')
        # Now import data for Hotel
        imported_data = self.resource.import_data(
            self.dataset,
            raise_errors=True
        )
        self.assertFalse(imported_data.has_errors())
        self.assertEquals(len(imported_data.rows), 1)

        imported_object = Hotel.objects.get(name='test-name')
        self.assertEquals(imported_object.city, city)
