from rest_framework import serializers

from hotels.models import City


class CitySerializer(serializers.ModelSerializer):
    """
    API serializer class to be used by :view: `api.CityAPIView`
    """
    class Meta:
        model = City
        fields = ('name', 'abbrv')
