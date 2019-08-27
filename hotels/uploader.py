import requests, csv
from apscheduler.schedulers.background import BackgroundScheduler

from django.conf import settings

from .models import City, Hotel


scheduler = BackgroundScheduler()


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
    """
    listed_data = get_csv_as_list(settings.HOTEL_CSV)
    for elem in listed_data:
        city = City.objects.get(abbrv=elem[0])
        hotel, _ = Hotel.objects.get_or_create(
            city=city,
            loc=elem[1],
            name=elem[2],
        )


@scheduler.scheduled_job('interval', minutes=5)
def run_cron_job():
    """
    Runs a cron job in order so that
    cities are imported before hotels.
    """
    write_list_to_city_model()
    write_list_to_hotel_model()


scheduler.start()
