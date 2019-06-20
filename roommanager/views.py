from django.contrib.auth.decorators import login_required
from django.forms import TimeField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from roommanager.models import Slots, Rooms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from roommanager import get_ical_ids
from roommanager.forms import RoomForm
from roommanager import dbaccess
import datetime
import time
import pytz
from time import gmtime, strftime, ctime

from django.db import models
def download_and_analyse(request):
    # num_icals = get_ical_ids.download_icals();
    num_icals = 285
    event_json = get_ical_ids.analyse_icals(1, num_icals, 'first')
    dbaccess.add_rooms(event_json)
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


@login_required(login_url='login/')
def main(request):
    return render(request, 'main.html')


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
    if request.method == 'POST':
        form = RoomForm(request.POST, request=request)
        if form.is_valid():
            myentry = Slots(starttime=datetime.datetime.now(), endtime=(datetime.datetime.now()+form.duration),
                            group=form.groupName, user=request.user)
            myentry.save()
            #myroom = Rooms(slotid=myentry, date=datetime.datetime.now(), room=id)
            return render(request, 'main.html')
    else:
        form = RoomForm()

    return render(request, 'room.html', {'form': form})
