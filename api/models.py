from django.db import models
from django.conf import settings
from django.utils import timezone
import os
from datetime import date, datetime
import time

DAYS_OF_WEEK = (
    (0, 'Понедельник'),
    (1, 'Вторник'),
    (2, 'Среда'),
    (3, 'Четверг'),
    (4, 'Пятница'),
    (5, 'Суббота'),
    (6, 'Воскресенье'),
)


class Role(models.Model):
    name = models.TextField(default='') 

    def __str__(self):
        return self.name

class User(models.Model):
    phone = models.TextField(default='')
    password = models.TextField(default='')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.phone


class Schedule(models.Model):
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    def __str__(self):
        day = dict(DAYS_OF_WEEK)
        day = day.get(int(self.day))
        
        return day + ": " + str(self.start_time) + " - " + str(self.end_time)

class Service(models.Model):
    price = models.IntegerField(default=0)
    name = models.TextField(default='')
    description = models.TextField(default='')
    days = models.ManyToManyField(Schedule, null=True, blank=True)
    limit_people = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.TextField(default='') 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(default='')
    qr_url = models.TextField(default="")
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    latitude = models.DecimalField(decimal_places=14, max_digits=16, blank=True, null=True)
    longitude = models.DecimalField(decimal_places=14, max_digits=16, blank=True, null=True)
    services = models.ManyToManyField(Service, null=True, blank=True)
    def __str__(self):
        return self.name

class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(default=datetime.today())
    end_time = models.DateTimeField(null=True, blank=True)
    close_timer = models.BooleanField(default=False)

    def start_timer(self):
        while(not self.close_timer):
            if(self.end_time < datetime.today()):
                break
            time.sleep(1)
        self.delete()

    def end_timer(self):
        self.close_timer = True

class TrainTimer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(default=datetime.today())
    end_time = models.DateTimeField(null=True, blank=True)
    close_timer = models.BooleanField(default=False)
    minutes = models.IntegerField(default=0)
    def start_timer(self):
        count = 0
        while(not self.close_timer):
            if(self.end_time < datetime.today()):
                break
            time.sleep(60)
            count += 1
            self.minutes = count

    def end_timer(self):
        self.close_timer = True
        price = self.minutes * company.price
        return price



