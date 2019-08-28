import subprocess
from apscheduler.schedulers.background import BlockingScheduler

# the base scheduler to which all cron jobs will be added
scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=30)
def subprocess_to_update_models_from_csv():
    """
    Calls a subprosses on the custom command `jobs` which can
    be found under `hotels.management.commands.jobs.py`.

    The subprocess is scheduled to run at intervals of 30 minutes.
    """
    subprocess.call('python manage.py jobs', shell=True, close_fds=True)

scheduler.start()
