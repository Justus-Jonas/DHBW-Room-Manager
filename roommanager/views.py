from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from roommanager.models import Slots, Rooms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from roommanager import get_ical_ids
from roommanager import dbaccess
import datetime

from django.db import models
def download_and_analyse(request):
    get_ical_ids.download_icals();
    event_json = get_ical_ids.analyse_icals(1, 284, 'first')
    dbaccess.add_rooms(event_json)


def test_model(request, room_name):
    room = Rooms.objects.filter(room=room_name)

    return render(request, 'models_test.html', room)


def delete_models(request):
    Rooms.objects.all().delete()
    return render(request, 'delete.html')

def retrieve_all(request):
    all_entries_rooms = Rooms.objects.all()
    all_entries_slots = Slots.objects.all()
    context_dict = {'content': all_entries_rooms, 'slot_list': all_entries_slots}
    return render(request, 'all.html', context_dict)


def retrieve_actual_date(request):
    date = datetime.datetime.now()
    cur_date = date.strftime("%Y-%m-%d")
    room = Rooms.objects.filter(room="Raum 117D", date=cur_date)

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
