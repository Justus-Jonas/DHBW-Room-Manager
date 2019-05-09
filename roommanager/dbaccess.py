from django.db import models

def add_rooms(event_json):
    for room, date_json in event_json.items():
        for date, time_list in date_json.items():
            for start_time, end_time in time_list:
                print("add room: " + room + " date: " + date + " stime: " + start_time + " etime: " + end_time)
