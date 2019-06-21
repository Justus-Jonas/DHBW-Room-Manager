from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from roommanager.openweather import getCurrentWeather
from roommanager.get_ical_ids import download_and_analyse
"""Scheduler for Weather API Calls and Icals Update"""
def start():
    sched = BlockingScheduler()
    scheduler = BackgroundScheduler()
    """Getting the latest temperature every 3 hours"""
    scheduler.add_job(getCurrentWeather, 'interval', hours=3)
    """Updating the icals every day at 2am"""
    sched.add_job(download_and_analyse, 'cron', hour=2)
    scheduler.start()

