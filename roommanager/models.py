from django.db import models

class Slots(models.Model):
    starttime = models.TimeField()
    endtime = models.TimeField()
    group = models.CharField(max_length=100)

    def __str__(self):
        return self.starttime + " - " + self.endtime

class Rooms(models.Model):
    room = models.CharField(max_length=100)
    date = models.DateField()
    slotid = models.ForeignKey(Slots, on_delete=models.CASCADE)

    def __str__(self):
        return self.room + ": " + self.date

class Forecast(models.Model):
    forecastdate = models.DateField()
    forecasttime = models.TimeField()
    temp = models.FloatField()