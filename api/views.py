from rest_framework import generics

from hotels.models import City
from .serializers import CitySerializer


class CityAPIView(generics.ListAPIView):
    """
    Basic api view that queries all objects in :model: `hotels.City`
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
