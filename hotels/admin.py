from django.contrib import admin

from import_export.admin import ImportExportModelAdmin, ImportMixin

from .models import City, Hotel
from .resources import CityResource, HotelResource
from .formats import (
    SCSV,
    return_preferred_import_formats,
)


@admin.register(City)
class CityAdmin(ImportExportModelAdmin, ImportMixin):
    resource_class = CityResource
    list_display = ('abbrv', 'name')

    def get_import_formats(self):
        """
        Returns import file formats that can be
        selected when importing data from the
        admin site
        """
        return return_preferred_import_formats()


@admin.register(Hotel)
class HotelAdmin(ImportExportModelAdmin, ImportMixin):
    resource_class = HotelResource
    list_display = ('name', 'city', 'loc')

    def get_import_formats(self):
        """
        Returns import file formats that can be
        selected when importing data from the
        admin site
        """
        return return_preferred_import_formats()
