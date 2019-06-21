from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from roommanager.openweather import getCurrentWeather


def start():
    sched = BlockingScheduler()
    scheduler = BackgroundScheduler()
    scheduler.add_job(getCurrentWeather, 'interval', hours=3)
    scheduler.start()
    #sched.add(#updateFunktionHierReinRestPräpraiert, 'cron', hour=2)