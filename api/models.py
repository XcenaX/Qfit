from django.db import models
from django.conf import settings
from django.utils import timezone
import os
from datetime import date, datetime
import time
from datetime import timedelta
from adminpanel.models import *
from adminpanel.modules.functions import broadcast_ticks
from api.modules.functions import get_random_string_of_numbers
from qfit.yandex_s3_storage import ClientDocsStorage

import string    
import random
from collections import Counter
DAYS_OF_WEEK = (
    ("0", 'Понедельник'),
    ("1", 'Вторник'),
    ("2", 'Среда'),
    ("3", 'Четверг'),
    ("4", 'Пятница'),
    ("5", 'Суббота'),
    ("6", 'Воскресенье'),
)



CODE_LENGTH = 5

#import pyrebase
import os
#from django.core.files.storage import default_storage
#from qfit.settings import config
# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()




class Role(models.Model):
    name = models.TextField(default='') 

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.TextField(default='') 

    def __str__(self):
        return self.name

class User(models.Model):
    phone = models.TextField(default='')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True, default=Role.objects.get(name="user").id)
    avatar = models.TextField(blank=True, null=True, default="")
    ref_code = models.TextField(default="", blank=True, null=True)
    bonuses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    telegram_id = models.IntegerField(default=0)
    month_bonuses = models.IntegerField(default=0)
    friends = models.ManyToManyField("User", null=True, blank=True, related_name="app_friends")
    telegram_friends = models.ManyToManyField("User", null=True, blank=True, related_name="telegram")
    email = models.TextField(default="")
    name = models.TextField(default="")
    second_name = models.TextField(default="")
    sex = models.TextField(default="")#no
    last_numbers = models.TextField(blank=True, null=True, default="")
    card_token = models.TextField(blank=True, null=True, default="")
    card_type = models.TextField(blank=True, null=True, default="")
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True, default=City.objects.all()[0].id)
    
    def is_currently_training(self):
        user = User.objects.filter(id=self.id).first()
        if len(TrainTimer.objects.filter(user=user)) == 0:
            return False
        return True

    def current_train(self):
        user = User.objects.get(id=self.id)
        train_timer = TrainTimer.objects.filter(user=user).first()
        if not train_timer:
            return None
        return {            
            "transaction_id": train_timer.transaction_id,
            "start_time": str(train_timer.start_time),
            "company": train_timer.company.id,            
        }

    def __str__(self):
        return self.phone + " | " + self.name + " " + self.second_name + " | " + str(self.id)

    def give_bonuses(self):
        for friend in self.friends.all():
            friend.bonuses += self.month_bonuses//10
            friend.save()  
        self.month_bonuses = 0  

    def generate_ref_code(self):
        ref_code_length = 8
        code_unique = False
        while not code_unique:
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = ref_code_length))
            if len(User.objects.filter(ref_code=ran))==0:
                code_unique = True
        self.ref_code = ran
        self.save()

    def trains_count(self):
        current_user = User.objects.get(pk=self.pk)
        return len(FinishedTrain.objects.filter(user = current_user))
    
    def avarage_train_time(self):
        current_user = User.objects.get(pk=self.pk)
        trains = FinishedTrain.objects.filter(user=current_user)
        count = len(trains)
        if count == 0:
            return 0
        minutes = 0
        for train in trains:
            minutes += train.minutes
        return minutes // count
    
    def max_train_time(self):
        current_user = User.objects.get(pk=self.pk)
        trains = FinishedTrain.objects.filter(user=current_user)
        if len(trains) == 0:
            return 0
        max_time = trains[0].minutes
        for train in trains:
            if max_time < train.minutes:
                max_time = train.minutes
        return max_time
    
    def most_visited_club(self):
        current_user = User.objects.get(pk=self.pk)
        trains = FinishedTrain.objects.filter(user=current_user)
        if len(trains) == 0:
            return None
        names = []
        for train in trains:
            names.append(train.company.name)
        count = Counter(names)
        return list(count.most_common()[0])[0]

class VerificationPhone(models.Model):
    phone = models.TextField(null=True, blank=True)
    code = models.TextField(default="")

    def generate_code(self):
        code_length = 8
        code_unique = False
        ran = ""
        while not code_unique:
            ran = get_random_string_of_numbers(CODE_LENGTH)
            if len(VerificationPhone.objects.filter(code=ran))==0:
                code_unique = True
        self.code = ran
        self.save()

    def __str__(self):
        return self.phone + " | " + self.code


class TimeLine(models.Model):
    start_time = models.TimeField(default=datetime.strptime("00:00", "%H:%M"))
    end_time = models.TimeField(default=datetime.strptime("00:01", "%H:%M"))
    price = models.IntegerField(default=0)
    company_id = models.IntegerField(null=True, blank=True)
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, null=True, blank=True)
    limit_people = models.IntegerField(default=0)
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

    def free_places(self):
        int_day = int(self.day)
        company = Company.objects.filter(id=self.company_id).first()
        if not company:
            return 0
        return self.limit_people - len(Timer.objects.filter(company=company, start_time=self.start_time, end_time=self.end_time, day=self.day))

    def __str__(self):
        return str(self.company_id) + " | " + self.get_fullname() + " | " + str(self.start_time) + " - " + str(self.end_time)

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
        day = day.get(self.day)
        
        return day

class MyImage(models.Model):
    image = models.FileField(storage=ClientDocsStorage(), blank=True, null=True)
    
from django.db.models import Count, Case, When, IntegerField
class ServiceCategory(models.Model):
    name = models.TextField(default='')
    image = models.FileField(storage=ClientDocsStorage(), blank=True, null=True)

    def count_trains(self):
        tag = ServiceCategory.objects.get(id=self.id)
        return len(Company.objects.filter(tags__in=[tag]).only("id"))

    def __str__(self):
        return self.name

# class Service(models.Model):
#     category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, blank=True, null=True)
#     description = models.TextField(default='')
#     days = models.ManyToManyField(Schedule, null=True, blank=True)
#     images = models.ManyToManyField(MyImage, null=True, blank=True)
#     def __str__(self):
#         return self.category.name

#     def get_price(self, day, time):
#         print(day)
#         current_day = self.days.filter(day=day).first()
#         print(current_day)
#         if not current_day:
#             return -1
#         current_timeline = current_day.timelines.all().filter(start_time__lte=time, end_time__gte=time).first()
#         if not current_timeline:
#             return -1
#         print(current_timeline)
        
#         return current_timeline.price
        
    # def days(self, model):
    #     return  model.days.all().order_by('day')

from decimal import Decimal
class Company(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal("5.0"))
    name = models.TextField(default='') 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(default='', blank=True, null=True)
    qr_url = models.TextField(default="", blank=True, null=True)
    latitude = models.DecimalField(decimal_places=14, max_digits=16, blank=True, null=True)
    longitude = models.DecimalField(decimal_places=14, max_digits=16, blank=True, null=True)
    #services = models.ManyToManyField(Service, null=True, blank=True)
    all_bonuses = models.IntegerField(default=0)
    description = models.TextField(default="", blank=True, null=True)
    avatar = models.FileField(storage=ClientDocsStorage(), blank=True, null=True)
    images = models.ManyToManyField(MyImage, null=True, blank=True)
    tags = models.ManyToManyField(ServiceCategory, null=True, blank=True)
    days = models.ManyToManyField(Schedule, null=True, blank=True)
    contacts = models.TextField(blank=True, null=True, default="")
    def get_price(self, day, time):
        
        current_day = self.days.filter(day=day).first()
        
        if not current_day:
            return -1
        current_timeline = current_day.timelines.all().filter(start_time__lte=time, end_time__gte=time).first()
        if not current_timeline:
            return -1
        
        
        return current_timeline.price

    def avarage_price(self):
        count = 0
        prices = 0
        for day in self.days.all():
            for timeline in day.timelines.all():
                count += 1
                prices += timeline.price
        if count == 0:
            return 0
        return prices // count

    # def save(self, *args, **kwargs):
        
    #     #obj_data['my_field'] = my_computed_value(obj_data['my_other_field'])   
    #     self.qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + str(self.id)

    #     days_list = [] 
    #     for count in range(0,7):                    
    #         days_list.append(Schedule.objects.create(day=count))
    #     self.days.add(*days_list)
        
    #     super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + " | " + str(self.id)

class FinishedTrain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    #service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    minutes = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    bill = models.IntegerField(default=0)
    def __str__(self):
        return self.user.phone + " | " + self.user.name + " | " +  str(self.end_time)

class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    #service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, blank=True, null=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, null=True, default=0)
    book_date = models.DateField(blank=True,null=True)

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
    
    # def delete_after_expired(self):
    #     print(datetime.now())
    #     if self.end_time < datetime.now.time():
    #         timer = Timer.objects.get(pk=self.pk)
    #         timer.delete()
    #         return True
    #     else:
    #         return False

    def __str__(self):
        return "(" + self.user.phone + ") " + str(self.start_time) + ": " + str(self.end_time) + " | " + str(self.book_date)

class TrainTimer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    #service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(default=datetime.today())
    end_time = models.DateTimeField(null=True, blank=True)
    transaction_id = models.TextField(blank=True, null=True, default="")        

    def __str__(self):
        return "(" + self.user.phone + ") " + self.company.name + ": " + str(self.start_time)
