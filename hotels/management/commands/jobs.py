from apscheduler.schedulers.background import BackgroundScheduler

from django.core.management.base import BaseCommand

from hotels.uploader import (
    write_list_to_city_model,
    write_list_to_hotel_model
)


scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', minutes=5)
class Command(BaseCommand):
    """Cron job to update models every five minutes"""
    write_list_to_city_model()
    write_list_to_hotel_model()

    def handle(self, *args, **kwargs):
        scheduler.start()
