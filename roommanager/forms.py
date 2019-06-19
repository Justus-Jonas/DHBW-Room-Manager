from django import forms
from django.forms import widgets

from roommanager.models import Rooms


class RoomForm(forms.Form):
    groupName = forms.CharField(label='Group name', max_length=50)
    #  start_time = forms.TimeField(widget=dhbwroommanager.SelectTimeWidget())
    #self.start_time = forms.TimeField(label="from")
    # #self.stop_time = forms.TimeField(label='to')
    #hourS = forms.ChoiceField(choices=[(x, x) for x in range(8, 21)])
    #hourS.label = "Start time"
    #minS = forms.ChoiceField(choices=[(x, x) for x in range(0, 60, 15)])
    #minS.label = "Mins"
    duration = forms.ChoiceField(choices=[(x, x) for x in range(15, 135, 15) if x < 60 or x % 30 == 0])
    duration.label = "Duration"
