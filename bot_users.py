import os, sys, time, getopt
import django
from django.conf import settings
from django.template.loader import render_to_string

os.environ.setdefault('DJANGO_SETTINGS_MODULE','qfit.settings')
django.setup()

from api.models import *

for user in User.objects.all():
    if user.telegram_id:
        print(user.phone)



