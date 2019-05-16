from django.db import models

class Slots(models.Model):
    starttime = models.TimeField()
    endtime = models.TimeField()

class Rooms(models.Model):
    room = models.CharField(max_length=100)
    date = models.DateField()
    slotid = models.ForeignKey(Slots, on_delete=models.CASCADE)

class Forecast(models.Model):
    forecastdate = models.DateField()
    forecasttime = models.TimeField()
    temp = models.FloatField()