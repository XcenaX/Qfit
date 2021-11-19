import os, sys, time, getopt
import django
from django.conf import settings
from django.template.loader import render_to_string

os.environ.setdefault('DJANGO_SETTINGS_MODULE','qfit.settings')
django.setup()

from api.models import *
from api.modules.sendEmail import send_email
from qfit.settings import EMAIL_HOST_USER

def get_args():
    date_from = None
    date_to = None
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["from=","to="])
    except getopt.GetoptError:
        print('top_users.py --from <dd.mm.yyyy> --to <dd.mm.yyyy>')
        sys.exit(2)
    for opt, arg in opts:
        if(opt == "--from"):
            date_from = datetime.strptime(arg, "%d.%m.%Y")
        elif(opt == "--to"):
            date_to = datetime.strptime(arg, "%d.%m.%Y")
        else:
            print('top_users.py --from <dd.mm.yyyy> --to <dd.mm.yyyy>')
            sys.exit(2)
    return date_from, date_to

DATE_FROM, DATE_TO = get_args()

def send_table(top):
    subject = "Рейтинг пользователей с " + str(DATE_FROM) + " до " + str(DATE_TO)
    message = render_to_string('top_users.html', {
        "top": top
    })
    send_email(message, subject, EMAIL_HOST_USER)

def count_and_minutes(user):
    minutes = 0
    count = 0
    for train in FinishedTrain.objects.filter(user=user, start_time__gte=DATE_FROM, start_time__lte=DATE_TO):
        minutes += train.minutes
        count += 1
    return count, minutes

top = []

for user in User.objects.all():
    count, minutes = count_and_minutes(user)
    top.append({
        "count": count,
        "minutes": minutes,
        "user": user,
        "points": count*minutes,
    })

sorted_top = sorted(top, key=lambda k: (k['minutes']*k["count"]), reverse=True) 

for user in sorted_top[0:20]:
    print(user["user"].name + " " + user["user"].second_name + " | " + user["user"].phone + " | " + "Тренировки: " + str(user["count"]) + " | Минуты: " + str(user["minutes"]) + " | Очки: " + str(user["points"]))

print("Высылаем таблицу на почту ", EMAIL_HOST_USER)
send_table(sorted_top[0:20])
    