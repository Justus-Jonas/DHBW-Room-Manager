import requests
import re
import os
import icalendar
import datetime
import pytz
from roommanager.dbaccess import add_rooms, update_rooms
download_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icals")


def download_icals():
    """Download Icals from vorlesungsplan.dhbw-mannheim.de"""
    index = 0
    ical_site = requests.get("https://vorlesungsplan.dhbw-mannheim.de/ical.php")
    ical_site = str(ical_site.content)
    UIDs = re.findall('[0-9]{7}', ical_site)
    is_new = True

    try:
        if len(os.listdir(download_path) ) == 0:
            var = ""
        else:
            var = 'i'
            is_new = False
    except FileNotFoundError:
        os.mkdir(download_path)

    for ids in UIDs:
        index += 1 #Starts with 1
        """Create Path for the Ical file"""
        download_url = os.path.join(download_path, var + str(index) + '.ical')
        url = "http://vorlesungsplan.dhbw-mannheim.de/ical.php?uid=" + ids
        if(len(download_path)) != len(UIDs):
            ical = requests.get(url)
            with open(download_url, 'wb') as f:
                print("download: " + url + " -> " + download_url)
                f.write(ical.content)
    return (index, is_new)


def analyse_ical_event(event_json, event):
    """Analysing the Icals"""
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

    # we are only interested in the future!
    if date < current_date():
        return;

    if location not in event_json:
        event_json[location] = {}

    timespan = (startdt.strftime("%H:%M"), enddt.strftime("%H:%M"))
    if date not in event_json[location]:
        event_json[location][date] = {timespan}
    else:
        event_json[location][date].add(timespan)


def analyse_icals(range1, range2, is_new):
    event_json = {}
    for x in range(range1, range2):
        if is_new:
            ical_name = os.path.join(download_path, str(x) + ".ical")
        else:
            ical_name = os.path.join(download_path, "i" + str(x) + ".ical")
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


def rotate_icals(num):
    for f in os.listdir(download_path):
        if re.search('^[0-9]+\.ical$', f):
            os.remove(os.path.join(download_path, f))

    for x in range(1, num+1):
        os.rename(os.path.join(download_path, 'i' + str(x) + ".ical"),
                  os.path.join(download_path, str(x) + ".ical"))


def download_and_analyse():
    (num_icals, is_new) = download_icals();
    # num_icals = 285
    # is_new = False
    event_json = analyse_icals(1, num_icals, is_new)
    if is_new:
        add_rooms(event_json)
    else:
        update_rooms(event_json)
        rotate_icals(num_icals)


def current_date():
    tz = pytz.timezone('Europe/Berlin')
    date = datetime.datetime.now(tz)
    date = date.strftime("%Y-%m-%d")
    return date;
