import requests
import re
import os
from datetime import datetime, timedelta, timezone
import icalendar
from dateutil.rrule import *
"""
allUIDs = []
coursesSubsite = requests.get("https://vorlesungsplan.dhbw-mannheim.de")
coursesSubsite = str(coursesSubsite.content)
coursesSubsiteIds = re.findall("gid=[0-9]*", coursesSubsite)
#print(coursesSubsiteIds)
for ids in coursesSubsiteIds:
    url = "https://vorlesungsplan.dhbw-mannheim.de/index.php?action=list&" + ids
    #print(url)
    curRequest = requests.get(url)
    courseSite = str(curRequest.content)
    #print(courseSite)
    courseSiteUids = re.findall("uid=[0-9]*", courseSite)
    courseSiteUids = str(courseSiteUids)
    allUIDs.append(str(courseSiteUids))

allUIDs = str(allUIDs)
allUIDs = allUIDs.replace("[", '')
allUIDs = allUIDs.replace("]", '')
allUIDs = allUIDs.replace("\"", '')
print(str(allUIDs))

#print(allGIDs)
#print(x)
"""

download_path = os.path.dirname(os.path.realpath(__file__)) + "\icals\\"
def download_icals():
    index = 0
    ical_site = requests.get("https://vorlesungsplan.dhbw-mannheim.de/ical.php")
    ical_site= str(ical_site.content)
    UIDs = re.findall('[0-9]{7}', ical_site)
    for ids in UIDs:
        print(ids)
        index += 1
        print(index)
        download_url = download_path + str(index) + '.ical'
        url = "http://vorlesungsplan.dhbw-mannheim.de/ical.php?uid=" + ids
        print(url)
        if(len(download_path)) != len(UIDs):
            ical = requests.get(url)
            with open(download_url, 'wb') as f:
                f.write(ical.content)



d = []
def analyse_icals():
    num_files = len([f for f in os.listdir(download_path)if os.path.isfile(os.path.join(download_path, f))])
    for x in range(1, 8):
        ical_name = download_path + str(x) + ".ical"
        #print(file_name)
        read_ical = open(ical_name, "rb")
        content = icalendar.Calendar.from_ical(read_ical.read())
        event_json = { }
        for event in content.walk():
            if event.name == "VEVENT":
                summary = event.get('summary')
                description = event.get('description')
                location = event.get('location')
                startdt = event.get('dtstart').dt
                enddt = event.get('dtend').dt
                exdate = event.get('exdate')
                #print ("Datum: {0} Zeitraum:{1}-{2} {3}\n".format(startdt.strftime("%m/%d/%Y"), startdt.strftime(" %H:%M "), enddt.strftime(" %H:%M "), location))
                location = location.replace("\'", '')
                location = location.replace("vText(b", '')
                if location not in event_json:
                    event_json[location] = []
                else:
                    event_json[location].append([startdt.strftime("%m/%d/%Y"), startdt.strftime("%H:%M"), enddt.strftime("%H:%M")])

            read_ical.close()
        print(event_json)



        #print(content)

analyse_icals()
"""
UIDs = str(UIDs)
UIDs = UIDs.replace('value=', '')
UIDs = UIDs.replace('\"', '')
print(UIDs[2:(UIDs.find(',')-2)])
print(UIDs)
for ids in UIDs:
    url = "http://vorlesungsplan.dhbw-mannheim.de/ical.php?uid=" + ids
    print(url)
    ical = requests.get(url)
    ical = str(ical.content)

"""
