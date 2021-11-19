
import random
import string
import datetime
from datetime import date, timedelta
import xlrd
from twilio.rest import Client 
from qfit.settings import TWILIO_SID, TWILIO_TOKEN, BASE_DIR, TWILIO_PHONE, MOBIZON_URL, MOBIZON_DOMAIN, MOBIZON_API_KEY
import os
IMAGE_TYPES = [".png", ".jpg", ".jpeg"]

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_random_string_of_numbers(length):
    letters = ["0","1","2","3","4","5","6","7","8","9"]
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def check_image_type(image):
    try:
        for image_type in IMAGE_TYPES:
            if image.name.endswith(image_type):
                return True
    except:
        return False
    return False

def check_timelines(schedules):
    for schedule in schedules:
        for another_timeline in schedule["timelines"]:
            for timeline in schedule["timelines"]:
                if timeline["id"] != another_timeline["id"]:
                    another_start_time = datetime.datetime.strptime(another_timeline["start_time"], "%H:%M")
                    another_end_time = datetime.datetime.strptime(another_timeline["end_time"], "%H:%M")
                    start_time = datetime.datetime.strptime(timeline["start_time"], "%H:%M")
                    end_time = datetime.datetime.strptime(timeline["end_time"], "%H:%M")
                    if another_start_time < start_time and another_end_time > start_time or another_start_time < end_time and another_end_time > end_time or another_end_time == end_time or another_start_time == start_time or another_end_time <= another_start_time or end_time <= start_time or another_start_time > start_time and another_end_time < end_time:
                        return False
    return True

def send_sms_twilio(to, message):
    account_sid = TWILIO_SID 
    auth_token = TWILIO_TOKEN
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(       
        body=message,      
        to=to,
        from_=TWILIO_PHONE
    ) 

import requests
from qfit.settings import SMSC_LOGIN, SMSC_PASSWORD, SMSC_URL

def send_smsc(to, message):
    #https://smsc.kz/sys/send.php?login=<login>&psw=<password>&phones=<phones>&mes=<message>
    url = SMSC_URL + "?login=" + SMSC_LOGIN + "&psw=" + SMSC_PASSWORD + "&phones=" + to + "&mes=" + message + "&sender=QFit.kz"
    url2 = SMSC_URL + "?login=" + SMSC_LOGIN + "&psw=" + SMSC_PASSWORD + "&phones=" + to + "&mes=" + message
    res = requests.get(url)    

def send_sms_mobizon(to, message):
    if to[0] == "+":
        to = to[1:]
    url = MOBIZON_URL + "?recipient="+to+"&text="+message+"&apiKey="+MOBIZON_API_KEY
    responce = requests.get(url)



def get_date_from_day(book_day):
    current_day = date.today().weekday()
    current_date = date.today()
    plus_date = 0
    while True:
        if current_day == book_day:
            current_date += timedelta(days=plus_date)
            break
        if current_day == 6:
            current_day = 0
        else:
            current_day += 1

        plus_date += 1
    return current_date

def remit_payment(info):
    #https://api.cloudpayments.ru/test
    #https://api.cloudpayments.ru/payments/cards/charge
    responce = requests.post("https://api.cloudpayments.ru/payments/cards/charge", data={
        "Amount": info["Amount"],
        "Currency": info["Currency"],
        "InvoiceId": info["InvoiceId"],
        "Description": info["Description"],
        "AccountId": info["AccountId"],
        "Name": info["AmoNameunt"],
    })
    responce = responce.json()
    if not responce["Success"]:
        if responce["Message"]:
            return {"error": responce["Message"]}
        elif responce["Model"]:
            return {"model": responce["Model"]}
    return {"success": True}



