from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from roommanager.openweather import getCurrentWeather
from roommanager.get_ical_ids import download_and_analyse

def start():
    sched = BlockingScheduler()
    scheduler = BackgroundScheduler()
    scheduler.add_job(getCurrentWeather, 'interval', hours=3)
    scheduler.start()
    sched.add_job(download_and_analyse, 'cron', hour=2)
