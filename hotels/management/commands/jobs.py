from apscheduler.schedulers.background import BackgroundScheduler

from django.core.management.base import BaseCommand

from hotels.uploader import (
    write_list_to_city_model,
    write_list_to_hotel_model
)


scheduler = BackgroundScheduler()


class Command(BaseCommand):
    write_list_to_city_model()
    write_list_to_hotel_model()

    @scheduler.scheduled_job('interval', seconds=30)
    def handle(self, *args, **kwargs):
        scheduler.start()
