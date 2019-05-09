from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from roommanager import get_ical_ids

def download_and_analyse():
    i = get_ical_ids.download_update_icals()
    get_ical_ids.analyse_icals(1, i, "new")


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
