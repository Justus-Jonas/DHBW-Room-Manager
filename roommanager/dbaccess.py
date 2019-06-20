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

@transaction.atomic
def update_rooms(event_json):
    print("clean slots")
    Slots.objects.all().delete()
    print("clean rooms")
    Rooms.objects.all().delete()
    add_rooms(event_json)

def room_status(room_name, duration = None):
    tz = pytz.timezone('Europe/Berlin')
    now = datetime.datetime.now(tz)
    #now = datetime.datetime.strptime("2019-06-21 13:00:00", "%Y-%m-%d %H:%M:%S")
    cur_date = now.strftime("%Y-%m-%d")
    room_info = Rooms.objects.filter(room=room_name, date=cur_date)

    if len(room_info) == 0:
        # print("room is free that day")
        return (True, None)

    if duration != None:
        end_time = now + datetime.timedelta(minutes = int(duration))
    else:
        end_time = now

    cur_date_obj = datetime.datetime.strptime(str(cur_date), "%Y-%m-%d")
    for t in room_info:
        # print("check: (" + str(now.time()) + "-" + str(now.time()) + "): " + str(t.slotid.starttime) +  "-" +  str(t.slotid.endtime))
        # print("combine: " + str(cur_date_obj) + " and " +str(datetime.datetime.strptime(str(t.slotid.starttime), "%H:%M:%S").time()))
        t_start = datetime.datetime.combine(cur_date_obj, datetime.datetime.strptime(str(t.slotid.starttime), "%H:%M:%S").time())
        # print("t_start: " + str(t_start))
        # print("now:     " + str(now))
        t_end = datetime.datetime.combine(cur_date_obj, datetime.datetime.strptime(str(t.slotid.endtime), "%H:%M:%S").time())
        # print("t_end:   " + str(t_end))
        # print("end_time:" + str(end_time))
        if t_end <= now.replace(tzinfo=None) or t_start >= end_time.replace(tzinfo=None):
            # print("not occupied")
            pass
        else:
            # print("occupied!")
            return (False, t.slotid)
    return (True, None)

def room_states_colors(roomnames):
    states = {}
    for room in roomnames:
        info = {'group': '', 'user': ''}
        (state, obj) = room_status(room)
        if state:
            (state, obj) = room_status(room, 15)
            if state:
                info['color'] = "rgba(124,252,0,0.5)"
                info['occupied'] = False
            else:
                info['color'] = "rgba(255,255,0,0.5)"
                info['occupied'] = True
                if obj.group != None:
                    info['group'] = obj.group
                    info['user'] = obj.user
        else:
            info['occupied'] = True
            if obj.group != None:
                info['group'] = obj.group
                info['user'] = obj.user
                info['color'] = "rgba(0,0,0,0.5)"
            else:
                info['color'] = "rgba(255,0,0,0.5)"
        states[room.replace(' ', '_')] = info
    return states
