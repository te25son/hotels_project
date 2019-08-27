from django.urls import path

from .views import CitySearchTemplateView, HotelListView


urlpatterns = [
    path('', CitySearchTemplateView.as_view(), name='search'),
    path('hotels/', HotelListView.as_view(), name='hotel_results'),
]
