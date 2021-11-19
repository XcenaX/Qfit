
from re import sub
from api.models import ServiceCategory
from api.models import *
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as Auth_User
import secrets
from django.shortcuts import render
from django.core.files import File
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from qfit.settings import BASE_DIR, STATIC_ROOT, TEST_ACCOUNT_PHONES
from django.db.models import Q

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from urllib.request import urlopen

from django.template.loader import render_to_string

from django.utils import dateparse, tree
import requests

from rest_framework.permissions import AllowAny

#from .filters import FoundItemFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from django.views.decorators.csrf import csrf_exempt

from tempfile import NamedTemporaryFile
import mimetypes

from api.modules.sendEmail import send_email

from django.http import HttpResponse, FileResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from datetime import timedelta
from datetime import date, datetime, timezone

import xlrd, xlwt

API_KEY = "AIzaSyCcHCB9lx35nurrIOy2KvphPIvmsflB4mE"

from adminpanel.modules.functions import broadcast_ticks, get_current_user
from .modules.functions import *

LIMIT_FRIENDS = 2

import pyrebase
import os
from django.core.files.storage import default_storage
from qfit.settings import config, HIDDEN_CLUBS_LIST



# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()



#storage.child("images/example.jpg").put("example.jpg")
#import googlemaps

# import mysql.connector
# from mysql.connector import Error
# import shutil

from .modules.hashutils import check_pw_hash, make_pw_hash
from adminpanel.models import *
import threading

TRAIN_EXPIRE = 240 # minutes


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CompanyViewSet(viewsets.ModelViewSet):
    #filter_backends = (SearchFilter, DjangoFilterBackend)
    #filter_fields = ["name", "tags__name", "contacts", "description", "address"]
    #authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Company.objects.exclude(id__in=HIDDEN_CLUBS_LIST)
    serializer_class = CompanySerializer

    def retrieve(self, request, pk=None):
        queryset = Company.objects.exclude(id__in=HIDDEN_CLUBS_LIST)
        try:
            item = Company.objects.get(id=pk)
            serializer = CompanySerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        description = self.request.query_params.get('description', None)
        address = self.request.query_params.get('address', None)
        tags = self.request.query_params.get('tagName', None)
        tag = self.request.query_params.get('tag', None)
        contacts = self.request.query_params.get('contacts', None)

        queryset = self.queryset.exclude(id__in=HIDDEN_CLUBS_LIST)
        if tag is not None:  
            tag = int(tag)          
            queryset = queryset.filter(tags__id__in=[tag])
        else:
            query = Q()
            if name is not None:
                query |= Q(name__icontains=name)
            if description is not None:
                query |= Q(description__icontains=description)
            if address is not None:
                query |= Q(address__icontains=address)
            if tags is not None:
                current_tag = ServiceCategory.objects.filter(name__icontains=tags).first()
                if current_tag:
                    query |= Q(tags=current_tag)
            if contacts is not None:
                query |= Q(contacts__icontains=contacts)
            queryset = queryset.filter(query)

        return queryset.exclude(id__in=HIDDEN_CLUBS_LIST)


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["phone", "role", "ref_code", "bonuses", "telegram_id"]
    http_method_names = ['get', 'post', 'head', 'put']
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            raise Http404

class AdminUserViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["username"]
    permission_classes = (IsAuthenticated,)
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer

    def retrieve(self, request, pk=None):
        queryset = AdminUser.objects.all()
        try:
            user = AdminUser.objects.get(id=pk)
            serializer = AdminUserSerializer(user)
            return Response(serializer.data)
        except:
            raise Http404

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, pk=None):
        queryset = Role.objects.all()
        try:
            role = Role.objects.get(id=pk)
            serializer = RoleSerializer(role)
            return Response(serializer.data)
        except:
            raise Http404


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, pk=None):
        queryset = Schedule.objects.all()
        try:
            schedule = Schedule.objects.get(id=pk)
            serializer = ScheduleSerializer(schedule)
            return Response(serializer.data)
        except:
            raise Http404

# class ServiceViewSet(viewsets.ModelViewSet):
#     filter_backends = (SearchFilter, DjangoFilterBackend)
#     filter_fields = ["category__name", "id"]
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     permission_classes = (IsAuthenticated,)
#     def retrieve(self, request, pk=None):
#         queryset = Service.objects.all()
#         try:
#             service = Service.objects.get(id=pk)
#             serializer = ServiceSerializer(service)
#             return Response(serializer.data)
#         except:
#             raise Http404

class FinishedTrainViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["company", "user", "start_time", "end_time"]
    permission_classes = (IsAuthenticated,)
    queryset = FinishedTrain.objects.all()
    serializer_class = FinishedTrainSerializer

    def retrieve(self, request, pk=None):
        queryset = FinishedTrain.objects.all()
        try:
            item = FinishedTrain.objects.get(id=pk)
            serializer = FinishedTrainSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class MyImageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = MyImage.objects.all()
    serializer_class = MyImageSerializer

    def retrieve(self, request, pk=None):
        queryset = MyImage.objects.all()
        try:
            item = MyImage.objects.get(id=pk)
            serializer = MyImageSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

class TimeLineViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TimeLine.objects.all()
    serializer_class = TimeLineSerializer

    def retrieve(self, request, pk=None):
        queryset = TimeLine.objects.all()
        try:
            item = TimeLine.objects.get(id=pk)
            serializer = TimeLineSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class TimerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["company", "user", "start_time", "end_time", "day"]
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer

    def retrieve(self, request, pk=None):
        queryset = Timer.objects.all()
        try:
            item = Timer.objects.get(id=pk)
            serializer = TimerSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class TrainTimerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TrainTimer.objects.all()
    serializer_class = TrainTimerSerializer

    def retrieve(self, request, pk=None):
        queryset = TrainTimer.objects.all()
        try:
            item = TrainTimer.objects.get(id=pk)
            serializer = TrainTimerSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # filter_backends = (SearchFilter, DjangoFilterBackend)
    # filter_fields = ["name"]
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

    def retrieve(self, request, pk=None):
        queryset = ServiceCategory.objects.all()
        try:
            item = ServiceCategory.objects.get(id=pk)
            serializer = ServiceCategorySerializer(item)
            return Response(serializer.data)
        except:
            raise Http404
    
    def get_queryset(self):
        name = self.request.query_params.get('name', None)

        queryset = self.queryset        
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
               
        return queryset

class DownloadFile(APIView):
    def get(self, request):
        fl_path = '/file/path'
        filename = 'downloaded_file_name.extension'

        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


class AddFriend(APIView):
    permission_classes = (IsAuthenticated,)  

    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})

    def post(self, request):
        current_user_id = int(request.POST["current_user"])
        code = request.POST["code"]
        current_user = None
        try:
            current_user = User.objects.get(id=current_user_id)
        except Exception as e:
            return Response({"error": "User with this id nit found!"})
        friend = None
        try:
            friend = User.objects.get(ref_code=code)        
        except Exception as e:
            return Response({"error": "User with this REF CODE nit found!"})
        

        if len(current_user.friends.all()) == 2:
            return Response({"error": "Максимальный лимит друзей "+ LIMIT_FRIENDS})
        if len(friend.friends.all()) == 2:
            return Response({"error": "У этого человека максимальный лимит друзей"})
        if len(current_user.friends.filter(ref_code=code)) > 0:
            return Response({"error": "Этот человек уже есть в списке друзей"})

        current_user.friends.add(friend)
        friend.friends.add(current_user)
        
        current_user.save()
        friend.save()
        
        return Response({"success": True}) 

@permission_classes((AllowAny, ))
class AddTelegramFriend(APIView):
    permission_classes = (IsAuthenticated,)  

    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})

    def post(self, request):
        current_user_id = int(request.POST["current_user"])
        code = request.POST["code"]
        current_user = None
        try:
            current_user = User.objects.get(telegram_id=current_user_id)
        except Exception as e:
            return Response({"error": "Неверный id пользователя!!"})
        friend = None
        try:
            friend = User.objects.get(ref_code=code)        
        except Exception as e:
            return Response({"error": "Неверный код!"})
                        
        if len(current_user.telegram_friends.filter(ref_code=code)) > 0:
            return Response({"error": "Этот человек уже есть в списке друзей!"})
        if current_user.id == friend.id:
            return Response({"error": "Вы не можете добавить себя в друзья!"})

        current_user.telegram_friends.add(friend)
        friend.telegram_friends.add(current_user)

        current_user.points += 3
        friend.points += 3
        
        current_user.save()
        friend.save()
        
        return Response({"success": True})

class CardData(APIView):
    permission_classes = (IsAuthenticated,)  

    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({"error": "User not found!"})
        return Response({"card_type": user.card_type, "last_numbers": user.last_numbers, "card_token": user.card_token})

    def post(self, request, id):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({"error": "User not found!"})
        card_type = request.POST["card_type"]
        last_numbers = request.POST["last_numbers"]
        card_token = request.POST["card_token"]

        user.card_type = card_type if card_type else user.card_type
        user.last_numbers = last_numbers if last_numbers else user.last_numbers
        user.card_token = card_token if card_token else user.card_token 
        user.save()

        return Response({"success": True}) 

class SendCode(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        phone = None
        # test
        try:
            phone = request.POST["phone"]
            
        except:
            return Response({"error": "Не передан один из параметров: phone"})
        message = None
        test_account = False
        is_exist = False
        if phone in TEST_ACCOUNT_PHONES:
            test_account = True

        phone2 = ""
        if phone.startswith("+"):
            phone2 = phone.replace("+", "", 1)
        elif phone.startswith("8"):
            phone2 = phone.replace("8", "7", 1)
        
        message = " код подтверждения в приложении QFit"            
        if len(User.objects.filter(Q(phone=phone) | Q(phone=phone2))) > 0:
            is_exist = True
                                                        
        # Выслать код
        another_verification = VerificationPhone.objects.filter(phone=phone).first()
        if another_verification:
            another_verification.delete()

        verification_phone = VerificationPhone.objects.create(phone=phone)
        if test_account:
            verification_phone.code = "91891"
            verification_phone.save()
        else:
            verification_phone.generate_code()                   
            message = verification_phone.code + message
            send_smsc(phone, message) 
            # СМСК

            #send_sms_mobizon(phone, message)
            # Мобизон
        return Response({"success": True, "is_exist": is_exist})

class UpdateTelegramIdByPhone(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        phone = None      
        try:
            phone = request.POST["phone"]     
            telegram_id = int(request.POST["telegram_id"])  
        except:
            return Response({"error": "Не передан один из параметров: phone, telegram_id"})
        
        try:
            user = User.objects.get(phone=phone)
            user.telegram_id = telegram_id
            user.save()
        except Exception as e:
            return Response({"error": e})
        return Response({"success": True})

class TopUsersByPoints(APIView):    
    def get(self, request):
        places = 10                    
        users = UserSerializer(User.objects.order_by("-points")[:places], many=True).data                       
        return Response(users)        
    def post(self, request):
        return Response({"error": request.method + " method not allowed!"})

class CheckCode(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        code = None
        phone = None
        try:
            code = request.POST["code"]
            phone = request.POST["phone"]
        except:
            return Response({"error": "Не передан один из параметров: code, phone"})
        
        verification_phone = VerificationPhone.objects.filter(phone=phone, code=code).first()
        if not verification_phone:
            return Response({"error": "Неправильный код!"})
        verification_phone.delete()
        phone2 = ""
        if phone.startswith("+"):
            phone2 = phone.replace("+7", "8", 1)
        else:
            phone2 = phone.replace("8", "+7", 1)
        user = User.objects.filter(Q(phone=phone) | Q(phone=phone2)).first()
        avatar = None
        role = None
        if user:
            try:
                avatar = user.avatar.url
            except:
                pass
            try:
                role = user.role.name
            except:
                pass
                
            return Response({"success": True, "user":{
                "id": user.id,
                "phone": user.phone,
                "role": role,
                "avatar": avatar,
                "ref_code": user.ref_code,
                "bonuses": user.bonuses,
                "email": user.email,
                "name": user.name,
                "sex": user.sex
            }})
        else:
            return Response({"success": True})    
        
        
            

class Register(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        phone = None
        name = None
        email = None
        sex = None
        try:
            phone = request.POST["phone"]
            name = request.POST["name"]
            email = request.POST["email"]
            sex = request.POST["sex"]
        except:
            return Response({"error": "Не передан один из параметров: name, email, sex, phone"})
        
        if phone.startswith("+7"):
            phone = phone.replace("+7", "8")
        user = User.objects.create(phone=phone, name=name, email=email, sex=sex)
        user.generate_ref_code()
        user.save()
        return Response({"success": True, "user":{
            "id": user.id,
            "phone": user.phone,
            "ref_code": user.ref_code,
            "bonuses": user.bonuses,
            "email": user.email,
            "name": user.name,
            "sex": user.sex
        }})

class BookTime(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        user_id = int(request.POST["user_id"])
        company_id = int(request.POST["company_id"])
        start_time  = request.POST["start_time"]
        end_time  = request.POST["end_time"]
        day  = int(request.POST["day"])
        if len(start_time) == 5:
            start_time += ":00"
        if len(end_time) == 5:
            end_time += ":00"
        start_time = datetime.datetime.strptime(start_time, '%H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%H:%M:%S')
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "Not authorized!"})
        
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return JsonResponse({"error": "Company not exist!"})
        
        current_timeline = TimeLine.objects.filter(company_id=company.id, day=day, start_time=start_time, end_time=end_time).first()
        if not current_timeline:
            return JsonResponse({"error": "Такая бронь не найдена!"})
        
        if current_timeline.free_places() == 0:
            return JsonResponse({"error": "На это время мест нет!"})

        if len(Timer.objects.filter(user=user, company=company, day=day, start_time=start_time, end_time=end_time)) > 0:
            return JsonResponse({"error": "У вас уже есть бронь на это время!"})
        
        timer = Timer.objects.create(user=user,company=company, end_time=end_time, start_time=start_time, day=day, price=current_timeline.price, book_date=get_date_from_day(day))
        
        timer.save()
        
        broadcast_ticks({
            "new_book": True,
            "timer_id": timer.id,
            "timer_start": str(timer.book_date),
            "timer_end": str(request.POST["end_time"]),
            "timer_day": current_timeline.get_fullname(),
            "timer_user": timer.user.phone,
            "timer_user_name": timer.user.name,
            "company_id": timer.company.id,
        })
        return Response({"success": "Company was booked!"}, status=status.HTTP_200_OK)

class ConfirmBook(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        #"2021-05-13T09:48:22.899Z"
        user_id = int(request.POST["user_id"])
        company_id = int(request.POST["company_id"])
        current_time = request.POST["current_time"]
        transaction_id = request.POST["transaction_id"]
        date_current_time = dateparse.parse_datetime(current_time)
        print(current_time)
        if not date_current_time:
            return Response({"error": "Не найдена дата\n"+current_time, "current_time": current_time}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "Not authorized!"})
        
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response({"error": "Company not exist!"})
        
        #book_timer = Timer.objects.filter(user=user, company=company, day=str(date_current_time.weekday()), start_time__lte=(date_current_time+datetime.timedelta(minutes=30)).time(), end_time__gte=date_current_time.time()).first()
        book_timer = Timer.objects.filter(user=user, company=company, day=str(date_current_time.weekday()), start_time__lte=(date_current_time).time(), end_time__gte=date_current_time.time()).first()
        if not book_timer:            
            return Response({"error": "Бронь на этот телефон  на это время не не найдена!"})            
        else:
            timer = TrainTimer.objects.create(user=user,company=company, start_time=date_current_time, transaction_id=transaction_id)
            timer.save()
            book_timer.delete()
            #book_timer.delete()
            
            broadcast_ticks({
                "new_timer": True,
                "timer_id": timer.id,
                "timer_start": str(timer.start_time),
                "timer_user": timer.user.phone,
                "company_id": timer.company.id,
            })
            return Response({"success": "Тренировка началась!"})


class DeclineBook(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        timer_id = int(request.POST["timer_id"])
        timer = Timer.objects.filter(id=timer_id).first() 
        timer.delete()
        broadcast_ticks({
            "company_id": timer.company.id,
            "decline_book": True,
            "timer_id": timer_id,
        })
        return Response({"success": "Бронь подтверждена!"})

class EndTrain(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        user_id = int(request.POST["user_id"])
        company_id = int(request.POST["company_id"])
        current_time_str = request.POST["current_time"]
        
        # CardCryptogramPacket = request.POST.get("CardCryptogramPacket", None)
        # test = request.POST.get("test", None)
        # test = request.POST.get("test", None)
        # test = request.POST.get("test", None)
        # test = request.POST.get("test", None)

        
        current_time = dateparse.parse_datetime(current_time_str)
        
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "Not authorized!"})
        
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response({"error": "Company not exist!"})
        
        train_timer = TrainTimer.objects.filter(user=user, company=company).first()
        print(current_time)
        print(train_timer.start_time)
        minutes = (current_time - train_timer.start_time).seconds//60
        price = None
        if minutes <= 240:
            price = minutes * company.get_price(train_timer.start_time.weekday(), train_timer.start_time)
        else:
            price = TRAIN_EXPIRE * company.get_price(train_timer.start_time.weekday(), train_timer.start_time)
        if price < 0:
            return Response({"error": "Цена меньше нуля!"})
        transaction_id = train_timer.transaction_id
        finished_train = FinishedTrain.objects.create(start_time=train_timer.start_time, end_time=current_time, user=user, company=company, minutes=minutes, bill=price)
        finished_train.save()
        train_timer.delete()
        user.points += minutes
        friends_points = minutes//2
        for friend in user.telegram_friends.all():
            friend.points += friends_points
            friend.save()
        user.save()
        broadcast_ticks({
            "new_history": True,
            "phone": finished_train.user.phone,
            "start_time": str(finished_train.start_time),
            "end_time": str(finished_train.end_time),
            "minutes": minutes,
            "bill": finished_train.bill,
            "history_id": finished_train.id,
        })

        #Оплата
        # info = {
        #     "CardCryptogramPacket": CardCryptogramPacket,

        # }

        # remit_payment(info)
        
        
        return Response({"success": "Тренировка окончена!", "bill": price, "minutes": minutes, "transaction_id": transaction_id})

class GetMinutes(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        current_time_str = request.POST["current_time"]
        
        if len(current_time_str) == 16:
            current_time_str += ":10"
        current_time = dateparse.parse_datetime(current_time_str)
        train_timer_id = request.POST["timer_id"]
        train_timer = TrainTimer.objects.filter(id=int(train_timer_id)).first()
        if not train_timer:
            return Response({"error": "Train timer with ID " + train_timer_id + " not found!"})
        minutes = (current_time - train_timer.start_time).seconds//60
        return Response({"minutes": minutes})

class UpdateSchedules(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        tags_json = request.POST["tags"]
        tags = json.loads(tags_json)
        tags_list = []
        for tag in tags:
            int_tag = int(tag)
            tags_list.append(ServiceCategory.objects.get(id=int_tag))
        schedules_json = request.POST["schedules"]
        schedules = json.loads(schedules_json)
        
        current_user = get_current_user(request)
        
        current_user.company.description = request.POST["description"]
        current_user.company.contacts = request.POST["contacts"]
        current_user.company.tags.set(tags_list)
        tags = request.POST["tags"]
        current_user.company.save()
        if not check_timelines(schedules):
            return Response({"error": "Нельзя накладывать время занятия друг на друга!"})
        for schedule in schedules:
            current_schedule = current_user.company.days.all().filter(day=schedule["day"]).first()
            for timeline in schedule["timelines"]:
                db_timeline = TimeLine.objects.filter(id=timeline["id"]).first()
                
                if db_timeline:
                    start_time = datetime.datetime.strptime(timeline["start_time"], '%H:%M')
                    end_time = datetime.datetime.strptime(timeline["end_time"], '%H:%M')
                    
                    db_timeline.price = timeline["price"]
                    db_timeline.start_time = start_time
                    db_timeline.end_time = end_time
                    db_timeline.limit_people = timeline["limit_people"]
                    db_timeline.save()
            current_schedule.save()
        return Response({"success": "NICE BOY!"})


class AddTimeline(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        schedule_id = request.POST["schedule"]
        day = request.POST["day"]
        schedule = Schedule.objects.get(id=schedule_id)
        current_user = get_current_user(request)
        new_timeline = TimeLine.objects.create(company_id=current_user.company.id, day=day, limit_people=0)
        schedule.timelines.add(new_timeline)
        schedule.save()
        return Response({"id": new_timeline.id, "start_time": str(new_timeline.start_time)[:-3], "end_time": str(new_timeline.end_time)[:-3],  "price": new_timeline.price, "limit_people": 0})


class AddImage(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        # FIREBASE

        # url = request.POST.get("url", "")
        # company_id = int(request.POST["company"])
        # company = Company.objects.get(id=company_id)
        # model_image = MyImage.objects.create(image=url)
        # model_image.save()
        # company.images.add(model_image)
        # company.save()
        # return Response({"image": url, "id": model_image.id})

        #YANDEX CLOUD
        image = request.FILES.get("image", None)
        if not image:
            return Response({"error": "Не передано изображение!"})

        if(check_image_type(image) and image):
            current_user = get_current_user(request)
            model_image = MyImage.objects.create(image=image)
            model_image.save()
            
            current_user.company.images.add(model_image)
            current_user.company.save()
            return Response({"image": model_image.image.url, "id": model_image.id})
        else:
            upload_error = "Выберите .jpg, .jpeg или .png формат!" 
            return Response({"error": upload_error})

@permission_classes((AllowAny, ))
class SubmitReview(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"}, status=500)
    def post(self, request):
        text = request.POST.get("text", None)
        user_id = request.POST.get("user", None)
        callme = request.POST.get("callme", False)
        if not text or not user_id:
            return Response({"error": "Не передан один из параметров: text, user"}, status=500)
        user = None
        try:
            user = User.objects.get(id=user_id)
        except:
            pass
        if not user:
            return Response({"error": "User с таким id не найден"}, status=500)
        message = None
        subject = ""
        if callme:
            message = """
                Позвоните мне
                Телефон: {0}
                Имя: {1}
                Сообщение: {2}
            """.format(user.phone, user.name, text)
            subject = user.phone + ", " + user.name + " позвонить"
        else:
            message = """
                Отзыв
                Телефон: {0}
                Имя: {1}
                Сообщение: {2}
            """.format(user.phone, user.name, text)
            subject = user.phone + ", " + user.name + " отзыв"
        try:
            send_email(message, subject , settings.EMAIL_HOST_USER)
        except Exception as err:
            return Response({"error": "Проблема со входом в аккаунт gmail"}, status=500)    
        return Response({"success": True}, status=200)

@permission_classes((AllowAny, ))
class UpdateAvatar(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        #FIREBASE 

        # url = request.POST["url"]
        # company_id = int(request.POST["company"])
        # company = Company.objects.get(id=company_id)
        # company.avatar = url
        # company.save()
        # return Response({"image": url})
        
        # YANDEX CLOUD
        image = request.FILES.get("image", None)
        if not image:
            return Response({"error": "Не передано изображение!"})

        
        if(check_image_type(image) and image):
            current_user = get_current_user(request)
            current_user.company.avatar = image
            current_user.company.save()
            
            return Response({"image": current_user.company.avatar.url})
        else:
            upload_error = "Выберите .jpg, .jpeg или .png формат!" 
            return Response({"error": upload_error})

def xls_to_response(xls, fname):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response

def create_history_excel(company):
    trains = FinishedTrain.objects.filter(company=company)
    file_name = 'history_excel'+str(company.id)+'.xls'
    
    # if os.path.exists(file_name):
    #     os.remove(file_name)
    #with open(file_name, 'w'): pass # создаю файл для компании
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("History")

    worksheet.write(0,0, "Телефон")
    worksheet.write(0,1, "Имя")
    worksheet.write(0,2, "Дата брони")
    worksheet.write(0,3, "Время старта")
    worksheet.write(0,4, "Время окончания")
    worksheet.write(0,5, "Кол-во минут")
    worksheet.write(0,6, "Оплата")
    y = 1
    for train in trains:
        book_date = str(train.start_time.year) + "-" + str(train.start_time.month) + "-" + str(train.start_time.day)
        start_time = str(train.start_time.hour) + ":" + str(train.start_time.minute) + ":" + str(train.start_time.second)
        end_time = str(train.end_time.hour) + ":" + str(train.end_time.minute) + ":" + str(train.end_time.second)
        worksheet.write(y,0, train.user.phone)
        worksheet.write(y,1, train.user.name + " " + train.user.second_name)
        worksheet.write(y,2, book_date)
        worksheet.write(y,3, start_time)
        worksheet.write(y,4, end_time)
        worksheet.write(y,5, train.minutes)
        worksheet.write(y,6, train.bill)
        y+=1
    return workbook, file_name
    #return static_url

@permission_classes((AllowAny, ))
class DownloadExcel(APIView):
    def get(self, request, id):        
        company = None
        try:
            company = Company.objects.get(id=id)
        except:
            pass
        if not company:
            return Response({"error": "Компания с таким id не найдена!"})

        workbook, fname = create_history_excel(company)
        return xls_to_response(workbook, fname)
        #return Response({"url": static_url}, status=200)
    def post(self, request, id):        
        return Response({"error": request.method + " method not allowed!"})
        

@permission_classes((AllowAny, ))
class SubmitForm(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        club_name = request.POST["club_name"]
        description = request.POST["description"]
        city = request.POST["city"]
        #<input type="checkbox" name="has_optional_services" placeholder="Есть ли доп услуги">

        has_optional_services = request.POST.get("has_optional_services", "") 
        optional_services = request.POST["optional_services"]
        phone = request.POST["phone"]
        email = request.POST["email"]

        mail_subject = "Заявка на регистрацию клуба"
        message = render_to_string('submit_form_message.html', {
            'club_name': club_name,
            'description': description,
            'city': city,
            'has_optional_services': has_optional_services if has_optional_services else False,
            "optional_services": optional_services,
            "phone": phone,
            "email": email,
        })
        

        send_email(message, mail_subject, settings.EMAIL_HOST_USER)
        
        return Response({"success": True})

@permission_classes((AllowAny, ))
class SubmitQuestionForm(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        name = request.POST["name"]
        phone = request.POST["phone"]
        text = request.POST["message"]

        mail_subject = "Вопрос от " + name
        message = render_to_string('submit_question_form_message.html', {
            'name': name,
            'phone': phone,            
            "message": text
        })
        
        send_email(message, mail_subject, settings.EMAIL_HOST_USER)
        
        return Response({"success": True})

def test(request):
    return render(request, "test.html", {})


# @csrf_exempt
# def add_to_history(request):
#     if request.method == "POST":
        
        
#     return JsonResponse({"error": request.method + " method not allowed!"})


@receiver(models.signals.post_delete, sender=Company)
def company_avatar_delete_ondelete(sender, instance, using, **kwargs):
    instance.avatar.delete(save=False)

@receiver(models.signals.pre_save, sender=Company)
def company_avatar_delete_onsave(sender, instance, using, **kwargs):
    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False
    
    new_file = instance.avatar
    if not old_file == new_file:
        old_file.delete(save=False)

@receiver(models.signals.pre_delete, sender=MyImage)
def myimage_ondelete(sender, instance, using, **kwargs):
    instance.image.delete(save=False)


# @receiver(pre_delete, sender=MyImage)
# def item_delete(sender, instance, **kwargs):    
#     instance.image.delete(False)

# @receiver(pre_delete, sender=Document)
# def document_delete(sender, instance, **kwargs):
#     instance.image.delete(False)
