from rest_framework import generics

from hotels.models import City
from .serializers import CitySerializer


class CityAPIView(generics.ListAPIView):
    """
    Basic api view that queries all objects in :model: `hotels.City`

    The api view is used by jquery in the template `search.html` to
    auto-update and display all current citys in the database.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
