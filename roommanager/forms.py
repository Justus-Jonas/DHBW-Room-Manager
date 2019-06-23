from django import forms
from django.forms import widgets
from django.core import validators

from roommanager.models import Rooms
from roommanager.dbaccess import room_status


def get_room_from_request(id):
    return "Raum " + str(id)


class DurationField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(choices=[(x, x) for x in range(15, 135, 15) if x < 60 or x % 30 == 0])
        self.request = None

    def validate(self, value):
        super().validate(value)
        if self.request != None:
            # print("check")
            (state, _, _) = room_status(get_room_from_request(self.request), value)
            if state:
                # print("book")
                pass
            else:
                raise forms.ValidationError("occupied by someone else")
        else:
            raise forms.ValidationError("no underlying request")


class RoomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try:
            request = kwargs.pop("request")
        except:
            request = None
        super().__init__(*args, **kwargs)
        self.fields['duration'].request = request

    groupName = forms.CharField(label='Group name', max_length=50, validators=[validators.validate_slug])
    duration = DurationField()
    duration.label = "Duration"
