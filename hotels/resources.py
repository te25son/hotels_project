from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import City, Hotel


class CityResource(resources.ModelResource):
    """
    A resource from django-import-export used
    to import csv data directly to the :model:
    `hotels.City` model.
    """
    def before_import(self, dataset, *args, **kwargs):
        """
        Changes the headers of the given csv to match
        the fieldnames of the :model: `hotels.City` model
        by renaming the first row and appending the original
        row to the end of the file.
        """
        first_row = dataset.headers
        dataset.headers = ['abbrv', 'name']
        dataset.append(first_row)

    class Meta:
        model = City
        exclude = ('id',)
        import_id_fields = ('abbrv', 'name')


class HotelResource(resources.ModelResource):
    """
    A resource from django-import-export used
    to import csv data directly to the :model:
    `hotels.Hotel` model.
    """
    city = Field(
        column_name='city',
        attribute='city',
        widget=ForeignKeyWidget(City, 'abbrv'),
    )

    def before_import(self, dataset, *args, **kwargs):
        """
        Changes the headers of the given csv to match
        the fieldnames of the :model: `hotels.Hotel` model
        by renaming the first row and appending the original
        row to the end of the file.
        """
        first_row = dataset.headers
        dataset.headers = ['city', 'loc', 'name']
        dataset.append(first_row)

    class Meta:
        model = Hotel
        exclude = ('id',)
        import_id_fields = ('city', 'loc', 'name')
