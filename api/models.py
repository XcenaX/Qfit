from django.db import models
from django.conf import settings
from django.utils import timezone
import os
from datetime import date, datetime
import time
from datetime import timedelta
from adminpanel.models import *
from adminpanel.modules.functions import broadcast_ticks


import string    
import random

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
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True, default=Role.objects.get(name="user").id)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    ref_code = models.TextField(default="")
    bonuses = models.IntegerField(default=0)
    def __str__(self):
        return self.phone
    
    def generate_ref_code(self):
        ref_code_length = 8
        code_unique = False
        while not code_unique:
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = ref_code_length))
            if len(User.objects.filter(ref_code=ran))==0:
                code_unique = True
        self.ref_code = ran
        self.save()

class TimeLine(models.Model):
    start_time = models.TimeField(default=datetime.strptime("00:00", "%H:%M"))
    end_time = models.TimeField(default=datetime.strptime("00:01", "%H:%M"))
    limit_people = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

class Schedule(models.Model):
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    timelines = models.ManyToManyField(TimeLine, null=True, blank=True)

    def get_cutted_name(self):
        if(self.day == "0"):
            return "Пн"
        if(self.day == "1"):
            return "Вт"        
        if(self.day == "2"):
            return "Ср" 
        if(self.day == "3"):
            return "Чт"           
        if(self.day == "4"):
            return "Пт"          
        if(self.day == "5"):
            return "Сб"         
        if(self.day == "6"):
            return "Вс"
    
    def get_fullname(self):
        if(self.day == "0"):
            return "Понедельник"
        if(self.day == "1"):
            return "Вторник"        
        if(self.day == "2"):
            return "Среда" 
        if(self.day == "3"):
            return "Четверг"           
        if(self.day == "4"):
            return "Пятница"          
        if(self.day == "5"):
            return "Суббота"         
        if(self.day == "6"):
            return "Воскресенье"

    def __str__(self):
        day = dict(DAYS_OF_WEEK)
        day = day.get(int(self.day))
        
        return day

class MyImage(models.Model):
    image = models.ImageField(upload_to='services', blank=True, null=True)
    def __str__(self):
        return self.image.name

class ServiceCategory(models.Model):
    name = models.TextField(default='')
    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(default='')
    days = models.ManyToManyField(Schedule, null=True, blank=True)
    images = models.ManyToManyField(MyImage, null=True, blank=True)
    def __str__(self):
        return self.category.name

    def get_price(self, day, time):
        print(day)
        current_day = self.days.filter(day=day).first()
        print(current_day)
        if not current_day:
            return -1
        current_timeline = current_day.timelines.all().filter(start_time__lte=time, end_time__gte=time).first()
        if not current_timeline:
            return -1
        print(current_timeline)
        
        return current_timeline.price
        
    # def days(self, model):
    #     return  model.days.all().order_by('day')

class Company(models.Model):
    name = models.TextField(default='') 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(default='')
    qr_url = models.TextField(default="")
    latitude = models.DecimalField(decimal_places=14, max_digits=16, blank=True, null=True)
    longitude = models.DecimalField(decimal_places=14, max_digits=16, blank=True, null=True)
    services = models.ManyToManyField(Service, null=True, blank=True)
    def __str__(self):
        return self.name

class FinishedTrain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    minutes = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    bill = models.IntegerField(default=0)
    def __str__(self):
        return self.user.phone

class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(default=datetime.today())
    end_time = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    
    def delete_after_expired(self):
        print(datetime.now())
        if self.end_time < datetime.now():
            timer = Timer.objects.get(pk=self.pk)
            timer.delete()
            return True
        else:
            return False

    def __str__(self):
        return "(" + self.user.phone + ") " + self.company.name + ": " + str(self.end_time)

class TrainTimer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(default=datetime.today())
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "(" + self.user.phone + ") " + self.company.name + ": " + str(self.start_time)




