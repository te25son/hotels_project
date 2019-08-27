from django.urls import path

from .views import CityAPIView


urlpatterns = [
    path('', CityAPIView.as_view(), name='city_api'),
]
