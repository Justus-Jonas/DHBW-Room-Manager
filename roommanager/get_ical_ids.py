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
        download_url = download_path + "i" + str(index) + '.ical'
        url = "http://vorlesungsplan.dhbw-mannheim.de/ical.php?uid=" + ids
        print(url)
        if(len(download_path)) != len(UIDs):
            ical = requests.get(url)
            with open(download_url, 'wb') as f:
                f.write(ical.content)


def download_update_icals():
    prefix = "i"
    index = 0
    ical_site = requests.get("https://vorlesungsplan.dhbw-mannheim.de/ical.php")
    ical_site= str(ical_site.content)
    UIDs = re.findall('[0-9]{7}', ical_site)
    for ids in UIDs:
        print(ids)
        index += 1
        print(index)
        download_url = download_path + prefix + str(index) + '.ical'
        url = "http://vorlesungsplan.dhbw-mannheim.de/ical.php?uid=" + ids
        print(url)
        if(len(download_path)) != len(UIDs):
            ical = requests.get(url)
            with open(download_url, 'wb') as f:
                f.write(ical.content)
    return index
d = []
def analyse_icals(range1, range2, filenameflag):
    num_files = len([f for f in os.listdir(download_path)if os.path.isfile(os.path.join(download_path, f))])
    for x in range(range1, range2):
        if filenameflag == 'old':
            filename = download_path + str(x) + ".ical"
        else:
            filename = download_path + "i" + str(x) + ".ical"
        ical_name = filename
        #print(file_name)
        read_ical = open(ical_name, "rb")
        content = icalendar.Calendar.from_ical(read_ical.read())
        event_json = { }
        date_set = {}
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
                date_temp = str(startdt.strftime("%m/%d/%Y"))
                if location not in event_json:
                    event_json[location] = []
                if date_temp not in date_set:
                    date_set[date_temp] = []

                else:
                    date_set[date_temp].append([startdt.strftime("%H:%M"), enddt.strftime("%H:%M")])
                    event_json[location].append(date_set)

            read_ical.close()
        print(event_json)
        return event_json
        #print(date_set)


def update_icals():
    length = download_update_icals()
    for x in range(1, length):
        old_ical = download_path + str(x) + ".ical"
        new_ical = download_path + "i" + str(x) + ".ical"
        old_content = open(old_ical, "rb")
        new_content = open(new_ical, "rb")
        for line_old in old_content:
            for line_new in new_content:
                if line_new != line_old:
                    old_dict = analyse_icals(x, x, old_content)
                    new_dict = analyse_icals(x, x, new_content)
                    compare_dict(old_dict, new_dict)


                    #os.remove(old_ical)
                    #os.rename(new_ical, download_path + str(x) + ".ical")


        #print(content)


def compare_dict(old_dict, new_dict):
    oldd_keys = set(old_dict.keys())
    newd_keys = set(new_dict.keys())
    intersect_keys = oldd_keys.intersection(newd_keys)
    new_val = oldd_keys - newd_keys
    rem_val = newd_keys - oldd_keys
    mod_val = { i : (old_dict[i], new_dict[i]) for i in intersect_keys if old_dict[i] != new_dict[i]}
    print(new_val)
    print(rem_val)
    print(mod_val)
download_icals()


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
