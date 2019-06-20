from django import forms
from django.forms import widgets
from django.core import validators

from roommanager.models import Rooms
from roommanager.dbaccess import room_status


class DurationField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(choices=[(x, x) for x in range(15, 135, 15) if x < 60 or x % 30 == 0])
        self.request = None

    def validate(self, value):
        super().validate(value)
        if self.request != None:
            print("check")
            if room_status(self.request.path[6:-1]):
                print("book")
            else:
                print("can't book")
        else:
            print("fail")


class RoomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try:
            request = kwargs.pop("request")
        except:
            request = None
        super().__init__(*args, **kwargs)
        self.fields['duration'].request = request

    groupName = forms.CharField(label='Group name', max_length=50, validators=[validators.validate_slug])
    #  start_time = forms.TimeField(widget=dhbwroommanager.SelectTimeWidget())
    #self.start_time = forms.TimeField(label="from")
    # #self.stop_time = forms.TimeField(label='to')
    #hourS = forms.ChoiceField(choices=[(x, x) for x in range(8, 21)])
    #hourS.label = "Start time"
    #minS = forms.ChoiceField(choices=[(x, x) for x in range(0, 60, 15)])
    #minS.label = "Mins"
    duration = DurationField()
    duration.label = "Duration"
