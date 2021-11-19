import os, sys, time, getopt
import django
from django.conf import settings
from django.template.loader import render_to_string
import random
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE','qfit.settings')
django.setup()

from api.models import *

CHEAT_DATA = [(52, 250000), (53, 150000), (54, 100000), (55, 75000)] # (<id_клуба>, <до_какой_суммы_накрутить>)
DATE_FROM = "01-06-2021 "
DATE_TO = "02-07-2021 "


def get_start_time(timeline):
    month = random.randint(6,7)
    day = 0
    if month == 6:
        day = random.randint(1,30)
    else:
        day = random.randint(1,2)
    

def get_random_user():
    return User.objects.order_by('?')[0]

def get_random_timeline(club):
    day = random.randint(0,6)
    timelines = TimeLine.objects.filter(company_id=club.id, day=day)
    print(timelines)
    return timelines[random.randint(0, (len(timelines)-1))]
    

def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    
    ptime = stime + prop * (etime - stime)

    str_date = time.strftime(time_format, time.localtime(ptime))
    if str_date[11] == "0":
        int_hour = int(str_date[12])
        if int_hour < 8:
            str_date = list(str_date)
            str_date[12] = '9'
            str_date = "".join(str_date)

    if str_date[11] == "2" and str_date[12] == "2" or str_date[12] == "3":
        str_date = list(str_date)
        str_date[12] = '0'
        str_date = "".join(str_date)
    return str_date


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M:%S', prop)

def get_end_time(start_time_str, minutes):
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    return start_time + timedelta(minutes=minutes)

def create_random_train(club):
    user = get_random_user()
    timeline = get_random_timeline(club)
    train_time = random.randint(45, 184)
    bill = timeline.price * train_time
    start_time = random_date("2021-06-01 08:00:00", "2021-07-02 20:20:00", random.random())
    end_time = get_end_time(start_time, train_time)
    return FinishedTrain.objects.create(user=user, company=club, start_time=start_time, end_time=end_time, bill=bill, minutes=train_time)
    

    


for id, count in CHEAT_DATA:
    try:
        club = Company.objects.get(id=id)
    except:
        print("COmpany not found! Skip!")
        pass
    current_count = 0
    while current_count < count:
        train = create_random_train(club)
        print(train)
        current_count += train.bill


    