from django.contrib import admin

from import_export.admin import ImportExportModelAdmin, ImportMixin

from .models import City, Hotel
from .resources import CityResource, HotelResource


@admin.register(City)
class CityAdmin(ImportExportModelAdmin, ImportMixin):
    resource_class = CityResource
    list_display = ('abbrv', 'name')


@admin.register(Hotel)
class HotelAdmin(ImportExportModelAdmin, ImportMixin):
    resource_class = HotelResource
    list_display = ('name', 'city', 'loc')
