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
    password = models.TextField(default='')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    ref_code = models.TextField(default="")
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

class Service(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    days = models.ManyToManyField(Schedule, null=True, blank=True)
    images = models.ManyToManyField(MyImage, null=True, blank=True)
    def __str__(self):
        return self.name

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
    close_timer = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    def start_timer(self):
        while(not self.close_timer):
            if(self.end_time < datetime.today()):
                break
            time.sleep(60)
        broadcast_ticks({
            "book_expired": True,
            "timer_id": self.id,  
            "company_id": self.company.id,
        })
        Timer.objects.filter(id=self.id).first().delete()

    def end_timer(self):
        self.close_timer = True
        self.save()

    def __str__(self):
        return "(" + self.user.phone + ") " + self.company.name + ": " + str(self.end_time)

class TrainTimer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(default=datetime.today())
    end_time = models.DateTimeField(null=True, blank=True)
    close_timer = models.BooleanField(default=False)
    minutes = models.IntegerField(default=0)
    def start_timer(self):
        count = 0
        close_timer = False
        while(not close_timer):
            time.sleep(5)
            close_timer = TrainTimer.objects.get(id=self.id).close_timer
            if close_timer:
                break
            count += 1
            self.minutes = count
            self.save()
            timer = TrainTimer.objects.get(id=self.id)
            broadcast_ticks({"minutes": timer.minutes, "id": timer.id, "company_id": timer.company.id})
             
        TrainTimer.objects.get(id=self.id).delete()

    def end_timer(self):
        price = self.minutes * self.service.price
        finished_train = FinishedTrain.objects.create(start_time=self.start_time, end_time=self.start_time + timedelta(minutes=self.minutes), company=self.company, service=self.service, minutes=self.minutes, bill=price, user=self.user)
        finished_train.save()
        broadcast_ticks({
            "delete_id": self.id,
            "service_name": finished_train.service.name,
            "phone": finished_train.user.phone,
            "end_time": str(finished_train.end_time),
            "minutes": finished_train.minutes,
            "finished_train_id": finished_train.id,
            "company_id": finished_train.company.id,
            })
        return price

    def __str__(self):
        return "(" + self.user.phone + ") " + self.company.name + ": " + str(self.start_time)




