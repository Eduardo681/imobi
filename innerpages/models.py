from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    img = models.ImageField(upload_to='img')

    def __str__(self) -> str:
        return self.img.url


class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class VisitingDays(models.Model):
    day = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.day


class Time(models.Model):
    time = models.TimeField()

    def __str__(self) -> str:
        return str(self.time)


class Immobile(models.Model):
    choices = (('S', 'Sale'),
               ('R', 'Rent'))

    choices_immobile = (('A', 'Apartment'),
                        ('H', 'Home'))

    images = models.ManyToManyField(Image)
    value = models.FloatField()
    rooms = models.IntegerField()
    size = models.FloatField()
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    street = models.CharField(max_length=50)
    type = models.CharField(max_length=1, choices=choices)
    type_immobile = models.CharField(max_length=1, choices=choices_immobile)
    number = models.IntegerField()
    description = models.TextField()
    visiting_days = models.ManyToManyField(VisitingDays)
    times = models.ManyToManyField(Time)

    def __str__(self) -> str:
        return self.street


class Visits(models.Model):
    choices = (('S', 'Sunday'),
               ('M', 'Monday'),
               ('T', 'Tuesday'),
               ('W', 'Wednesday'),
               ('TH', 'Thursday'),
               ('F', 'Friday'),
               ('Sa', 'Saturday'))

    choices_status = (('S', 'Scheduled'),
                      ('F', 'Finished'),
                      ('C', 'Canceled'))
    immobile = models.ForeignKey(Immobile, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    day = models.CharField(max_length=20)
    time = models.TimeField()
    status = models.CharField(max_length=1, choices=choices_status, default="A")

    def __str__(self) -> str:
        return self.user.username
