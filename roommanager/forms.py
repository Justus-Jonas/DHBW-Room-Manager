from django import forms
from django.forms import widgets

from roommanager.models import Rooms


class RoomForm(forms.Form):
    class Meta:
        model = Rooms

    g_name = forms.CharField(label='Group name', max_length=50)
    #  start_time = forms.TimeField(widget=dhbwroommanager.SelectTimeWidget())
    #self.start_time = forms.TimeField(label="from")
    # #self.stop_time = forms.TimeField(label='to')
    hourS = forms.ChoiceField(choices=[(x, x) for x in range(8, 21)])
    hourS.label = "Start time"
    minS = forms.ChoiceField(choices=[(x, x) for x in range(0, 60, 15)])
    hourE = forms.ChoiceField(choices=[(x, x) for x in range(0, 3)])
    hourE.label = "Duration"
    minE = forms.ChoiceField(choices=[(x, x) for x in range(0, 60, 15)])

