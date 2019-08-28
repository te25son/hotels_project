from django.core.management.base import BaseCommand

from hotels.uploader import (
    write_list_to_city_model,
    write_list_to_hotel_model
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print("Sarting jobs command")
        write_list_to_city_model()
        write_list_to_hotel_model()
