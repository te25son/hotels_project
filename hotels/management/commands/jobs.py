from django.core.management.base import BaseCommand

from hotels.uploader import (
    write_list_to_city_model,
    write_list_to_hotel_model
)


class Command(BaseCommand):
    """
    A custom command that can be run with `python manage.py jobs`

    The custom command is used by jobs.py in the root directory
    for initiating cron jobs.
    """

    def handle(self, *args, **kwargs):
        """
        The fuctional part of the command.

        Runs two functions from hotels.uploads
        to read csv files over authenticated HTTP
        and populate the models City and Hotel with
        the read data.
        """
        write_list_to_city_model()
        write_list_to_hotel_model()
