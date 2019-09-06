import requests, csv

from django.conf import settings

from .models import City, Hotel


def get_csv_as_list(csv_file):
    """
    Using a csv file requested over authenticated http
    returns a nested list of the csv's data
    """
    listed_data = list()
    with requests.Session() as ses:
        data = ses.get(csv_file, auth=(settings.CSV_USERNAME, settings.CSV_PASSWORD))
        decoded_data = data.content.decode('utf-8')
        csv_reader = csv.reader(decoded_data.splitlines(), delimiter=';')
        listed_data = list(csv_reader)
    return listed_data


def write_list_to_city_model():
    """
    Using a nested list where each element
    is a list containing two elements (a city
    abbreviation and a city name), writes each
    element to the City model

    This function is used by the cron job (jobs.py)
    in the root directory. The function can be
    removed from the cron job by editing the
    custom command under hotels.management.commands.jobs.py
    """
    listed_data = get_csv_as_list(settings.CITY_CSV)
    for elem in listed_data:
        city, _ = City.objects.get_or_create(
            abbrv=elem[0],
            name=elem[1],
        )


def write_list_to_hotel_model():
    """
    With a nested list where each element
    is a list containing three elements (a city
    abbreviation, a location, and a name), writes
    each element to the Hotel model.

    This function is used by the cron job (jobs.py)
    in the root directory. The function can be
    removed from the cron job by editing the
    custom command under hotels.management.commands.jobs.py
    """
    listed_data = get_csv_as_list(settings.HOTEL_CSV)
    for elem in listed_data:
        hotel, _ = Hotel.objects.get_or_create(
            loc=elem[1],
            name=elem[2],
        )
        if _:
            hotel.objects.create(city=elem[0])
            
