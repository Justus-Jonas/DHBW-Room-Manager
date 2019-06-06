from django import forms
from django.forms import widgets


class RoomForm(forms.Form):
    class Meta:
        model = Rooms

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['mydate'].widget = widgets.AdminDateWidget()
        self.fields['mytime'].widget = widgets.AdminTimeWidget()
        self.fields['mydatetime'].widget = widgets.AdminSplitDateTime()
        g_name = forms.CharField(label='Group name', max_length=50)
        #  start_time = forms.TimeField(widget=dhbwroommanager.SelectTimeWidget())
        self.start_time = forms.TimeField(label="from")
        self.stop_time = forms.TimeField(label='to')
        # will be filled in by django
