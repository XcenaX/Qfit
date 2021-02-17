from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Service)
admin.site.register(Schedule)
admin.site.register(Role)
admin.site.register(Timer)
admin.site.register(TrainTimer)
# admin.site.register(Item)
# admin.site.register(Type)
# admin.site.register(Address)
# admin.site.register(Role)
# admin.site.register(Condition)
# admin.site.register(Order)
#admin.site.register(OrderStatus)