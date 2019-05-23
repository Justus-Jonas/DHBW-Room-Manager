from django.db import models
from roommanager.models import Slots, Rooms
from roommanager import get_ical_ids
def add_rooms(event_json):
    i = 0
    for room in event_json:
        for datejson in event_json[room]:
            for date, timelist in datejson.items():
                for start_time, end_time in timelist:
                    saveslots = Slots()
                    if start_time is None:
                        saveslots.starttime = '00:00'
                    else:
                        saveslots.starttime = start_time
                    if end_time is None:
                        saveslots.endtime = '00:00'
                    else:
                        saveslots.endtime = end_time
                    #saveslots.numb = i
                    saveslots.save()
                    saverooms = Rooms()
                    saverooms.room = room
                    saverooms.date = date
                    saverooms.slotid = saveslots
                    saverooms.save()
                    print(room + date +" " + start_time+" " + end_time+" " + str(i))
                    i += 1

"""
def show_room(room_name):
    Rooms.objects.filter(room=room_name)
"""
