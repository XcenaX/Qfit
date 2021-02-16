from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
#from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
import os
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *

router = routers.SimpleRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'schedules', ScheduleViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    # path("fill_document/", views.fill_document, name="fill_document"),
    # path("fill_waybill/", views.fill_waybill, name="fill_waybill"),
    # path("set_status/", views.set_status, name="set_status"),
    # path("test/", views.test, name="test"),
    # path("get_coords/", views.get_coords, name="get_coords"),
    # path("get_items/", views.get_items, name="get_items"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    #path("set_connection_info/", views.set_database_connection_info, name="set_connection_info"),
    
    #path('<str:filepath>/', views.download_file)
]

urlpatterns = format_suffix_patterns(urlpatterns)