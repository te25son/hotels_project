import json

from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from .serializers import CitySerializer
from hotels.models import City


# API client app
client = Client()


class APITests(TestCase):
    """Test module for API"""

    def setUp(self):
        City.objects.create(
            abbrv='NYC',
            name='New York'
        )
        self.response = client.get(reverse('city_api'))

    def test_view_response_status(self):
        self.assertEquals(self.response.status_code, 200)

    def test_response_uses_serialized_data(self):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        self.assertEquals(self.response.data, serializer.data)
