import requests
import re
import os
import icalendar
import datetime
#from roommanager.dbaccess import add_rooms
download_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icals")


def download_icals():
    index = 0
    ical_site = requests.get("https://vorlesungsplan.dhbw-mannheim.de/ical.php")
    ical_site= str(ical_site.content)
    UIDs = re.findall('[0-9]{7}', ical_site)

    try:
        if len(os.listdir(download_path) ) == 0:
            var = ""
        else:
            var = 'i'
    except FileNotFoundError:
        os.mkdir(download_path)

    for ids in UIDs:
        index += 1 #Starts with 1
        download_url = os.path.join(download_path, var + str(index) + '.ical')
        url = "http://vorlesungsplan.dhbw-mannheim.de/ical.php?uid=" + ids
        if(len(download_path)) != len(UIDs):
            ical = requests.get(url)
            with open(download_url, 'wb') as f:
                print("download: " + url + " -> " + download_url)
                f.write(ical.content)
    return index


def analyse_ical_event(event_json, event):
    location = event.get('location')
    if location == '':
        return

    summary = event.get('summary')
    # description = event.get('description')
    startdt = event.get('dtstart').dt
    enddt = event.get('dtend').dt
    # exdate = event.get('exdate')
    location = location.replace("\'", '')
    location = location.replace("vText(b", '')
    date = str(startdt.strftime("%Y-%m-%d"))

    if location not in event_json:
        event_json[location] = {}

    timespan = (startdt.strftime("%H:%M"), enddt.strftime("%H:%M"))
    if date not in event_json[location]:
        event_json[location][date] = {timespan}
    else:
        event_json[location][date].add(timespan)



def analyse_icals(range1, range2, filenameflag):
    event_json = {}
    for x in range(range1, range2):
        if filenameflag == 'first':
            ical_name = os.path.join(download_path, str(x) + ".ical")
        else:
            ical_name = os.path.join(download_path, i + str(x) + ".ical")
        print("analyse: " + ical_name)
        read_ical = open(ical_name, "rb")
        content = icalendar.Calendar.from_ical(read_ical.read())
        for event in content.walk():
            if event.name == "VCALENDAR":
                for event_t in event:
                    if event.name == "VEVENT":
                        analyse_ical_event(event_json, event_t)

            if event.name == "VEVENT":
                analyse_ical_event(event_json, event)
        read_ical.close()

    print("event_json (" + str(len(event_json)) + "): " + str(event_json.keys()))
    # with open("event_json.txt", "w") as f:
    #     f.write(str(event_json))
    return event_json


#FIXME: needs review
def update_icals(new_length):
    for x in range(1,new_length):
        old_ical = os.path.join(download_path, str(x) + ".ical")
        new_ical = os.path.join(download_path, "i" + str(x) + ".ical")
        try:
            new_content = open(new_ical, "rb")
        except FileNotFoundError:
            # no new file -> skip
            continue
        try:
            # new file and old file -> possibly apply merge
            old_content = open(old_ical, "rb")
        except FileNotFoundError:
            # only new file -> just add
            event_json = analyse_icals(x, x+1, "first")
            add_rooms(event_json)
            continue

        #Merge
        exit_loops = False
        for line_old in old_content:
            for line_new in new_content:
                if line_new != line_old:
                    old_dict = analyse_icals(x, x + 1, "first")
                    #print(old_dict)
                    new_dict = analyse_icals(x, x +1, "new")
                    #print(new_dict)
                    compare_dict(old_dict, new_dict)
                    exit_loops = True
                    break
                else:
                    print("okay")
            if exit_loops:
                break



def compare_dict(old_dict, new_dict):
    oldd_keys = set(old_dict.keys())
    newd_keys = set(new_dict.keys())
    intersect_keys = oldd_keys.intersection(newd_keys)
    new_val = oldd_keys - newd_keys
    rem_val = newd_keys - oldd_keys
    mod_val = { i : (old_dict[i], new_dict[i]) for i in intersect_keys if old_dict[i] != new_dict[i]}



def current_date():
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d")
    print(date)

current_date()

