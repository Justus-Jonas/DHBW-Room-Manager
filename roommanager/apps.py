from django.apps import AppConfig


class RoommanagerConfig(AppConfig):
    name = 'roommanager'

    def ready(self):
        from roommanager import scheduler
        scheduler.start()
