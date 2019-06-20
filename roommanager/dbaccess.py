from django.db import models, transaction
from roommanager.models import Slots, Rooms
import datetime
import pytz
from roommanager import get_ical_ids

@transaction.atomic
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
                saveslots.save()
                print(room + " " + date + " " + start_time + " " + end_time + " " + str(i))
                saverooms = Rooms()
                saverooms.room = room
                saverooms.date = date
                saverooms.slotid = saveslots
                saverooms.save()
                i += 1

def room_status(room_name):
    date = datetime.datetime.now()
    cur_date = date.strftime("%Y-%m-%d")
    room_info = Rooms.objects.filter(room=room_name, date=cur_date)

    if len(room_info) == 0:
        #TODO: throw
        return False

    tz = pytz.timezone('Europe/Berlin')
    current_time = date.now(tz)
    current_time = current_time.strftime("%H:%M:%S")
    #test_time = datetime.datetime.strptime("10:00:00", "%H:%M:%S")
    current_time = datetime.datetime.strptime(current_time, "%H:%M:%S")

    for t in room_info:
        print(t.slotid.endtime)
        t_start = datetime.datetime.strptime( str(t.slotid.starttime), "%H:%M:%S")
        t_end = datetime.datetime.strptime( str(t.slotid.endtime), "%H:%M:%S")
        if current_time >= t_start and current_time <= t_end:
            print("In time")
        else:
            print("Not in time")
            return False
    return True

"""
def show_room(room_name):
    Rooms.objects.filter(room=room_name)
"""
