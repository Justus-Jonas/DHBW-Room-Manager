from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from roommanager import get_ical_ids
from roommanager.forms import RoomForm


def download_and_analyse():
    i = get_ical_ids.download_icals()
    get_ical_ids.update_icals(i)


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
        # create a form instance and populate it with data from the request:
        form = RoomForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'main.html')
        # if a GET (or any other method) we'll create a blank form
    else:
        form = RoomForm()

    return render(request, 'room.html', {'form': form})
