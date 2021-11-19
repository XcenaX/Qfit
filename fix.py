import os, sys, time
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','qfit.settings')
django.setup()

from api.models import *

for company in Company.objects.all():
    for day in company.days.all():
        for timeline in day.timelines.all():
            timeline.company_id = company.id