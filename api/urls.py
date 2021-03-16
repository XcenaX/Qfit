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

from rest_framework_simplejwt import views as jwt_views

router = routers.SimpleRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'finished_trains', FinishedTrainViewSet)
router.register(r'images', MyImageViewSet)
router.register(r'timelines', TimeLineViewSet)

from rest_framework.authtoken import views as api_views

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
    path("test/", views.test, name="test"),
    path("book_time/", views.book_time, name="book_time"),
    path("confirm_book/", views.confirm_book, name="confirm_book"),
    path("end_train/", views.end_train, name="end_train"),
    path("accept_book/", views.accept_book, name="accept_book"),
    path("decline_book/", views.decline_book, name="decline_book"),
    path("update_schedules/", views.update_schedules, name="update_schedules"),
    path("add_image/", views.add_image, name="add_image"),
    path("add_service/", views.add_service, name="add_service"),
    path("add_timeline/", views.add_timeline, name="add_timeline"),
    path('token/', api_views.obtain_auth_token, name='api-token-auth'),
    #path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    #path("set_connection_info/", views.set_database_connection_info, name="set_connection_info"),
    
    #path('<str:filepath>/', views.download_file)
]

urlpatterns = format_suffix_patterns(urlpatterns)