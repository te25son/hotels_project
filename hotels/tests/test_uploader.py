import requests

from django.test import TestCase
from django.conf import settings
from django.core.management import call_command

from ..uploader import (
    get_csv_as_list,
    write_list_to_city_model,
    write_list_to_hotel_model,
)
from ..models import City, Hotel


class UploaderTests(TestCase):

    def setUp(self):
        self.city_csv = requests.get(
            settings.CITY_CSV,
            auth=(settings.CSV_USERNAME, settings.CSV_PASSWORD)
        )
        self.hotel_csv = requests.get(
            settings.HOTEL_CSV,
            auth=(settings.CSV_USERNAME, settings.CSV_PASSWORD)
        )

    def test_connection_to_csv_files(self):
        self.assertEquals(self.city_csv.status_code, 200)
        self.assertEquals(self.hotel_csv.status_code, 200)

    def test_city_csv_rows_are_correct_length(self):
        """
        Test rows in CITY_CSV to match the number of fields in City model
        """
        listed_data = get_csv_as_list(settings.CITY_CSV)
        for elem in listed_data:
            self.assertEquals(len(elem), 2)

    def test_hotel_csv_rows_are_correct_length(self):
        """
        Test rows in HOTELS_CSV to match the number of fields in Hotel model
        """
        listed_data = get_csv_as_list(settings.HOTEL_CSV)
        for elem in listed_data:
            self.assertEquals(len(elem), 3)

    def test_city_csv_written_to_city_model(self):
        """
        Checks that the City model is being updated by the CSV
        """
        # check City model is first empty
        self.assertEquals(City.objects.all().count(), 0)

        # get length of listed data to tell us how many objects will be uploaded
        data_len = len(get_csv_as_list(settings.CITY_CSV))
        write_list_to_city_model()
        self.assertEquals(City.objects.all().count(), data_len)

    def test_hotel_csv_written_to_hotel_model(self):
        """
        Checks that the Hotel model is being updated by the CSV
        """
        # check City model is first empty
        self.assertEquals(Hotel.objects.all().count(), 0)

        # write city models so foreignkey works
        write_list_to_city_model()

        # get length of listed data to tell us how many objects will be uploaded
        data_len = len(get_csv_as_list(settings.HOTEL_CSV))
        write_list_to_hotel_model()
        self.assertEquals(Hotel.objects.all().count(), data_len)

    def test_first_element_in_city_csv_is_abbrv(self):
        """
        Checks that the first element in the city csv
        is an abrreviation of three letters
        """
        listed_data = get_csv_as_list(settings.CITY_CSV)
        for elem in listed_data:
            self.assertEquals(len(elem[0]), 3)

    def test_hotel_name_updated(self):
        """
        Tests that the hotel name is updated if the
        name is updated on the csv and no new objects
        have been created
        """
        # call custom command to download data
        call_command('jobs')
        hotel = Hotel.objects.get(pk=1)
        hotel.name = 'Test Name'
        hotel.save()
        hotel_count = Hotel.objects.all().count()

        self.assertEquals(hotel.name, 'Test Name')

        # call command to update hotel model
        # this should update the name of the object we just changed
        write_list_to_hotel_model()
        try:
            hotel = Hotel.objects.get(name='Test Name')
        except:
            hotel = None
            
        self.assertFalse(isinstance(hotel, Hotel))
        self.assertEquals(hotel_count, Hotel.objects.all().count())
