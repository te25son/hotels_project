from rest_framework import generics

from hotels.models import City
from .serializers import CitySerializer


class CityAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
