from django.db import models
from roommanager.models import Slots, Rooms
def add_rooms(event_json):
    i = 0
    for room in event_json:
        for datejson in event_json[room]:
            for date, timelist in datejson.items():
                for start_time, end_time in timelist:
                    saveslots = Slots(starttime=start_time, endtime=end_time)
                    saveslots.save()
                    saverooms = Rooms(room=room, date=date, slotid=i)
                    saverooms.save()
                    #print(room + date +" " + start_time+" " + end_time+" " + str(i))
                    i += 1
