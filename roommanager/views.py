from django.contrib.auth.decorators import login_required
from django.forms import TimeField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from roommanager.models import Slots, Rooms, Forecast
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from roommanager import get_ical_ids
from roommanager.forms import RoomForm, get_room_from_request
from roommanager import dbaccess
from roommanager import openweather
import datetime
import time
from django.core.exceptions import ObjectDoesNotExist
import pytz
from time import gmtime, strftime, ctime
from django.contrib import messages


def download_and_analyse(request):
    get_ical_ids.download_and_analyse()
    return render(request, 'all.html', {'rooms': Rooms.objects.all()})


def test_model(request, room_name):
    room = Rooms.objects.filter(room=room_name)
    return render(request, 'models_test.html', room)


def delete_models(request):
    Rooms.objects.all().delete()
    return render(request, 'all.html', {'rooms': Rooms.objects.all()})


def retrieve_all(request):
    return render(request, 'all.html', {'rooms': Rooms.objects.all()})


def retrieve_slot_inf(request):
    date = datetime.datetime.now()
    cur_date = date.strftime("%Y-%m-%d")
    room = Rooms.objects.filter(room="Raum 114D", date=cur_date)
    room_dict = {'information': room}
    tz = pytz.timezone('Europe/Berlin')
    current_time = date.now(tz)
    current_time = current_time.strftime("%H:%M:%S")
    #test_time = datetime.datetime.strptime("10:00:00", "%H:%M:%S")
    current_time = datetime.datetime.strptime(current_time, "%H:%M:%S")
    for t in room_dict.get('information'):
        print(t.slotid.endtime)
        t_start = datetime.datetime.strptime( str(t.slotid.starttime), "%H:%M:%S")
        t_end = datetime.datetime.strptime( str(t.slotid.endtime), "%H:%M:%S")
        if current_time >= t_start and current_time <= t_end:
            print("In time")
        else:
            print("Not in time")
    return render(request, 'actualdate.html', room_dict)



def retrieve_actual_date(request):
    date = datetime.datetime.now()
    cur_date = date.strftime("%Y-%m-%d")
    print(cur_date)
    room = Rooms.objects.filter(room="Raum 114D", date=cur_date)

    room_dict = {'information': room}
    return render(request, 'actualdate.html', room_dict)


def get_main_dict():
    return dbaccess.room_states_colors([
         "Raum 067C",
         "Raum 068C",
         "Raum 069C",
         "Raum 070C",
         "Raum 066C",
         "Raum 065C",
         "Raum 064C",
         "Raum 063C",
         "Raum 050B",
         "Raum 051B",
         "Raum 049B",
         "Raum 048B",
         "Raum 036B",
         "Raum 035B",
         "Raum 034B",
         "Raum 033B",
         "Raum 037B",
         "Raum 038B",
         "Raum 039B",
         "Raum 040B",
         "Raum 041B"
        ])


@login_required(login_url='login/')
def main(request):
    return render(request, 'main.html', {'states': get_main_dict(), 'weather': get_temp()})


def get_temp():
    try:
        fc = Forecast.objects.all()[:1].get()
    except:
        openweather.getCurrentWeather()
        fc = Forecast.objects.all()[:1].get()
    return fc.temp


def sign(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'sign.html', {'form': form})


def room_form(request, id):
    tz = pytz.timezone('Europe/Berlin')
    now = datetime.datetime.now(tz).replace(microsecond=0)
    # now = datetime.datetime.strptime("2019-06-25 15:00:00", "%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        form = RoomForm(request.POST, request=request)
        if form.is_valid():
            slot = Slots(starttime=now,
                        endtime=(now + datetime.timedelta(minutes=int(form.data['duration']))),
                        group=form.data['groupName'],
                        user=request.user.username)
            slot.save()
            room = Rooms(slotid=slot, date=now.strftime("%Y-%m-%d"), room=get_room_from_request(id))
            room.save()
            print("add room: " + room.room + " " + str(room.date) + " " + str(room.slotid) + " " + slot.group)
            return render(request, 'main.html', {'states': get_main_dict()})
    else:
        form = RoomForm()
    rooms = Rooms.objects.filter(date=now.strftime("%Y-%m-%d"), room=get_room_from_request(id))
    s = []
    time = (now + datetime.timedelta(hours=3))
    for r in rooms:
        if (r.slotid.endtime >= now.time() and r.slotid.endtime <= time.time()) or \
                (r.slotid.starttime >= now.time() and r.slotid.endtime <= time.time()) or \
                (r.slotid.starttime >= now.time() and r.slotid.starttime <= time.time()) or \
                (r.slotid.starttime <= now.time() and r.slotid.endtime >= time.time()):
            if r.slotid.group:
                s.append([str(r.slotid), str(r.slotid.group)])
            else:
                s.append([str(r.slotid), "BLOCKED"])
    states = get_main_dict()
    try:
        user = states["Raum_" + id]['user']
        if user != '' or states["Raum_" + id]['occupied']:
            bookable = False
        else:
            bookable = True
    except:
        bookable = True
    return render(request, 'room.html', {'form': form, 'states': states,
                                         'rooms': s,
                                         'room': get_room_from_request(id),
                                         'weather': get_temp(),
                                         'bookable': bookable})


def slots_delete_view(request, id):
    (status, slot) = dbaccess.room_status("Raum " + id)
    if status:
        return redirect('/room/' + id)

    if request.method == "POST" and request.user.username == slot.user:
        slot.delete()
        messages.success(request, "Reservation successfully revoked!")
        return redirect('main')
    return render(request, 'delete.html', {'slot': slot, 'states': get_main_dict(),
                                           'weather': get_temp()})

