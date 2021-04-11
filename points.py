import os, sys, time
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','qfit.settings')
django.setup()

from api.models import *
from datetime import datetime
import json
import time
from django.utils import timezone

for user in User.objects.all():
    user.give_bonuses()
