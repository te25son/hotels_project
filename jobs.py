import subprocess
from apscheduler.schedulers.background import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=30)
def subprocess_to_update_models_from_csv():
    subprocess.call('python manage.py jobs', shell=True, close_fds=True)

scheduler.start()
