from django.db import models
from roommanager.models import Slots, Rooms
from roommanager import get_ical_ids

def add_rooms(event_json):
    i = 0
    for room, date_dict in event_json.items():
        for date, timespan_tuple in date_dict.items():
            for start_time, end_time in timespan_tuple:
                saveslots = Slots()
                if start_time is None:
                    saveslots.starttime = '00:00'
                else:
                    saveslots.starttime = start_time
                if end_time is None:
                    saveslots.endtime = '00:00'
                else:
                    saveslots.endtime = end_time
                # saveslots.save()
                print(room + " " + date + " " + start_time + " " + end_time + " " + str(i))
                saverooms = Rooms()
                saverooms.room = room
                saverooms.date = date
                saverooms.slotid = saveslots
                # saverooms.save()
                i += 1
    saveslots.save()
    saverooms.save()

"""
def show_room(room_name):
    Rooms.objects.filter(room=room_name)
"""
