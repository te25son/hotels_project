from django.test import TestCase
from django.urls import reverse, resolve

from ..views import CitySearchTemplateView, HotelListView
from ..models import City, Hotel


class CitySearchTemplateViewTests(TestCase):

    def setUp(self):
        self.url = reverse('search')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_uses_correct_view_class(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, CitySearchTemplateView)

    def test_uses_correct_template(self):
        self.assertEquals(self.response.template_name, ['search.html'])

    def test_view_has_input(self):
        self.assertContains(self.response, '<input', 1)


class HotelListViewTests(TestCase):

    def setUp(self):
        self.url = reverse('hotel_results')
        self.response = self.client.get(self.url)
        city = City.objects.create(
            abbrv='NYC',
            name='New York',
        )
        hotel = Hotel.objects.create(
            city=city,
            loc='NYC99',
            name='The Plaza',
        )

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_uses_correct_view_class(self):
        view = resolve('/hotels/')
        self.assertEquals(view.func.view_class, HotelListView)

    def test_query_objects_with_data(self):
        response = self.client.get(self.url, {'q': 'New York'})
        self.assertContains(response, 'Hotels in New York')
        self.assertContains(response, '<table')
        self.assertContains(response, 'The Plaza')
        self.assertContains(response, 'NYC99')
        self.assertContains(response, 'Oh no!', 0) # does not contain

    def test_query_objects_without_data(self):
        response = self.client.get(self.url, {'q': 'Amsterdam'})
        self.assertContains(response, 'Hotels in Amsterdam')
        self.assertContains(response, '<table', 0) # does not contain
        self.assertContains(response, 'Oh no!')

    def test_blank_query_object(self):
        response = self.client.get(self.url, {'q': ''})
        self.assertContains(response, 'Hotels')
        self.assertContains(response, 'Hotels in', 0)
        self.assertContains(response, '<table')  # returns all hotels in database

    def test_has_link_back_to_seach_view(self):
        search_view = reverse('search')
        self.assertContains(self.response, f'href="{search_view}"')
