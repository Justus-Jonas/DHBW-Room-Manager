from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

from roommanager.models import Rooms
from roommanager.openweather import getCurrentWeather
from roommanager.get_ical_ids import download_and_analyse

"""Scheduler for Weather API Calls and Icals Update"""
startup = False


def start():
    if not startup and len(Rooms.objects.all()) == 0:
        download_and_analyse()
        getCurrentWeather()
    scheduler = BackgroundScheduler()
    """Getting the latest temperature every hour"""
    scheduler.add_job(getCurrentWeather, 'interval', hours=1)
    """Updating the icals every day at 2am"""
    scheduler.add_job(download_and_analyse, 'cron', hour=2)
    scheduler.start()
