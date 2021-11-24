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
router.register(r'adminusers', AdminUserViewSet)
router.register(r'roles', RoleViewSet)
#router.register(r'services', ServiceViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'finished_trains', FinishedTrainViewSet)
router.register(r'images', MyImageViewSet)
router.register(r'timelines', TimeLineViewSet)
router.register(r'timers', TimerViewSet)
router.register(r'train_timers', TrainTimerViewSet)
router.register(r'service_categories', ServiceCategoryViewSet)


from rest_framework.authtoken import views as api_views

urlpatterns = [
    url(r'^', include(router.urls)),
    # path("fill_document/", views.fill_document, name="fill_document"),
    # path("fill_waybill/", views.fill_waybill, name="fill_waybill"),
    # path("set_status/", views.set_status, name="set_status"),
    # path("test/", views.test, name="test"),
    # path("get_coords/", views.get_coords, name="get_coords"),
    # path("get_items/", views.get_items, name="get_items"),
    path("check_code/", views.CheckCode.as_view(), name="check_code"),
    path("send_code/", views.SendCode.as_view(), name="send_code"),
    path("register/", views.Register.as_view(), name="register"),
    path("test/", views.test, name="test"),
    path("book_time/", views.BookTime.as_view(), name="book_time"),
    path("confirm_book/", views.ConfirmBook.as_view(), name="confirm_book"),
    path("get_minutes/", views.GetMinutes.as_view(), name="get_minutes"),
    path("end_train/", views.EndTrain.as_view(), name="end_train"),
    path("decline_book/", views.DeclineBook.as_view(), name="decline_book"),
    path("update_schedules/", views.UpdateSchedules.as_view(), name="update_schedules"),
    path("add_image/", views.AddImage.as_view(), name="add_image"),
    path("update_avatar/", views.UpdateAvatar.as_view(), name="update_avatar"),
    path("add_timeline/", views.AddTimeline.as_view(), name="add_timeline"),
    path("submit_form/", views.SubmitForm.as_view(), name="submit_form"),
    path("submit_question_form/", views.SubmitQuestionForm.as_view(), name="submit_question_form"),
    path("submit_review/", views.SubmitReview.as_view(), name="submit_review"),
    path("download_excel/<int:id>", views.DownloadExcel.as_view(), name="download_excel"),
    path("download_all_excel", views.DownloadAllExcel.as_view(), name="download_all_excel"),    
    path("add_friend/", views.AddFriend.as_view(), name="add_friend"),
    path("add_telegram_friend/", views.AddTelegramFriend.as_view(), name="add_telegram_friend"),    
    path('token/', api_views.obtain_auth_token, name='api-token-auth'),
    path('card_data/<int:id>', views.CardData.as_view(), name='card_data'),
    path('update_telegram_id', views.UpdateTelegramIdByPhone.as_view(), name='update_telegram_id'),
    path('top_users', views.TopUsersByPoints.as_view(), name='top_users'),    
    #path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    #path("set_connection_info/", views.set_database_connection_info, name="set_connection_info"),
    
    #path('<str:filepath>/', views.download_file)
    #
]

urlpatterns = format_suffix_patterns(urlpatterns)