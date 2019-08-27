from django.test import TestCase
from django.urls import reverse, resolve

from ..views import CitySearchTemplateView, HotelListView


class CitySearchTemplateViewTests(TestCase):

    def setUp(self):
        self.url = reverse('search')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_uses_correct_template(self):
        self.assertEquals(self.response.template_name, ['search.html'])


class HotelListViewTests(TestCase):

    def setUp(self):
        self.url = reverse('hotel_results')

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        print(self.response.content)
