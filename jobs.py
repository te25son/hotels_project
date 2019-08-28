from apscheduler.schedulers.background import BackgroundScheduler

from hotels.uploader import (
    write_list_to_city_model,
    write_list_to_hotel_model
)


scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', minutes=5)
def update_models_from_csv():
    """
    Runs a cron job in order so that
    cities are imported before hotels.
    """
    write_list_to_city_model()
    write_list_to_hotel_model()


scheduler.start()
