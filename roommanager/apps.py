from django.apps import AppConfig
import sys


class RoommanagerConfig(AppConfig):
    name = 'roommanager'

    def ready(self):
        from roommanager import scheduler
        if sys.argv[1] == 'runserver':
            scheduler.start()
