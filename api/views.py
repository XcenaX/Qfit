
from api.models import *
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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
from qfit.settings import BASE_DIR

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from urllib.request import urlopen

import requests

#from .filters import FoundItemFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from django.views.decorators.csrf import csrf_exempt

from tempfile import NamedTemporaryFile
import mimetypes

from django.http import HttpResponse, FileResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from datetime import timedelta
from datetime import datetime, date
API_KEY = "AIzaSyCcHCB9lx35nurrIOy2KvphPIvmsflB4mE"

from adminpanel.modules.functions import broadcast_ticks, get_current_user
from .modules.functions import check_image_type, check_timelines

#import googlemaps

# import mysql.connector
# from mysql.connector import Error
# import shutil

from .modules.hashutils import check_pw_hash, make_pw_hash

import threading

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CompanyViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "services"]
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def retrieve(self, request, pk=None):
        queryset = Company.objects.all()
        try:
            item = Company.objects.get(id=pk)
            serializer = CompanySerializer(item)
            return Response(serializer.data)
        except:
            raise Http404


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["phone", "role"]
    authentication_classes = [CsrfExemptSessionAuthentication]
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


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
    def retrieve(self, request, pk=None):
        queryset = Schedule.objects.all()
        try:
            schedule = Schedule.objects.get(id=pk)
            serializer = ScheduleSerializer(schedule)
            return Response(serializer.data)
        except:
            raise Http404

class ServiceViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "id"]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    def retrieve(self, request, pk=None):
        queryset = Service.objects.all()
        try:
            service = Service.objects.get(id=pk)
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        except:
            raise Http404

class FinishedTrainViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["company", "service", "user", "start_time", "end_time"]
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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

@csrf_exempt
def download_file(request):
    fl_path = '/file/path'
    filename = 'downloaded_file_name.extension'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

@csrf_exempt
def fill_document(request):
    if request.method == "POST":
        item_id = request.POST["id"]
        if not item_id: 
            return JsonResponse({"error": "Parameter id is required!"})
        item = Purchased_Item.objects.filter(id=item_id).first()
        if not item:
            error = "Item with id=" + item_id + " not found!"
            return JsonResponse({"error": error})
        
        font = ImageFont.truetype( BASE_DIR + '//media//fonts//cmunss.ttf', 35)

        img = Image.open(BASE_DIR + "//media//dogovor.jpg").convert("RGB")

        draw = ImageDraw.Draw(img)
        draw.text((135, 415), item.item.provider.company.name, (0,0,0), font=font)
        draw.text((254, 1307), str(item.get_total_price()) + "тг", (0,0,0), font=font)
        draw.text((374, 1535), item.item.name, (0,0,0), font=font)
        draw.text((234, 1595), str(item.count) + " едениц", (0,0,0), font=font)

        absolute_path = BASE_DIR + "//media//dogovors//" + str(item.id) + ".jpg"
        img.save(absolute_path)

        document_path = "media/dogovors/" + str(item.id) + ".pdf"

        item.document.image = document_path
        item.document.save()
        return FileResponse(open(absolute_path, 'rb'), content_type='application/png')
    return JsonResponse({"error": "Only POST method is allowed!"})

@csrf_exempt
def fill_waybill(request):
    if request.method == "POST":
        order_id = request.POST["id"]
        if not order_id: 
            return JsonResponse({"error": "Parameter id is required!"})
        order = Order.objects.filter(id=order_id).first()
        if not order:
            error = "Order with id=" + order_id + " not found!"
            return JsonResponse({"error": error})
        
        font = ImageFont.truetype( BASE_DIR + '//media//fonts//cmunss.ttf', 25)

        img = Image.open(BASE_DIR + "//media//nakladnaya.jpg").convert("RGB")

        draw = ImageDraw.Draw(img)
        draw.text((590, 125), str(order.id), (0,0,0), font=font)
        draw.text((50, 350), "1", (0,0,0), font=font)
        draw.text((120, 350), order.item.name, (0,0,0), font=font)
        draw.text((480, 350), str(order.count), (0,0,0), font=font)
        draw.text((570, 350), str(order.item.price) + " тг", (0,0,0), font=font)
        draw.text((700, 350), str(order.get_total_price()) + " тг", (0,0,0), font=font)
        draw.text((130, 165), order.client_name, (0,0,0), font=font)

        absolute_path = BASE_DIR + "//media//waybills//" + str(order.id) + ".jpg"
        img.save(absolute_path)

        document_path = "media/waybills/" + str(order.id) + ".pdf"
        if not order.document:
            order.document = Document.objects.create()
        order.document.image = document_path
        order.document.save()
        return FileResponse(open(absolute_path, 'rb'), content_type='application/png')
    return JsonResponse({"error": "Only POST method is allowed!"})

def test(request):
    return render(request, "test.html", {})

@csrf_exempt
def set_status(request):
    if request.method == "POST":
        item_to_buy_id = request.POST["id"]
        
        if not item_to_buy_id:
            return JsonResponse({"error": "id parameter required!"})
        item = Purchased_Item.objects.filter(id=item_to_buy_id).first()
        
        if not item:
            return JsonResponse("Item with id not found!")
        if item.status is True:
            return JsonResponse({"error": "This item is already delivered!"})
        item.status = True
        item.save()

        new_item = Item.objects.create(name=item.item.name, item_type=item.item.item_type, receive_date=datetime.now(), provider=item.item.provider, price=item.item.price, count=item.count, image=item.item.image)
        new_item.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": request.method + " method not allowed!"})


@csrf_exempt
def get_coords(request):
    if request.method == "POST":
        name = ""
        try:
            name = request.POST["name"]
            data = requests.post("https://maps.googleapis.com/maps/api/geocode/json?address=" + name + "&key="+API_KEY)
            
            if data.json()["status"] == "ZERO_RESULTS":
                return JsonResponse({"error": "Not found!"})
            
            return JsonResponse({
                "longitude": data.json()["results"][0]["geometry"]["location"]["lng"],
                "latitude": data.json()["results"][0]["geometry"]["location"]["lat"]
                })
        except Exception as error:
            print(error)
            return JsonResponse({"error": str(error)})

    return JsonResponse({"error": request.method + " method not allowed!"})


@csrf_exempt
def register(request):
    if request.method == "POST":
        role_id = request.POST.get("role")
        role = Role.objects.filter(id=role_id).first()
        phone = request.POST["phone"]
        password = request.POST["password"]

        if len(User.objects.filter(phone=phone)) > 0:
            return JsonResponse({"error": "User with this phone already exist!"})
        user = User.objects.create(phone=phone, role=role, password=make_pw_hash(password))
        user.save()
        return JsonResponse({"success": True}) 

    return JsonResponse({"error": request.method + " method not allowed!"})


@csrf_exempt
def login(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        password = request.POST["password"]
        users = User.objects.filter(phone=phone)
        if len(users) == 0:
            return JsonResponse({"error": "User with this phone doesn't exist!"})
        user = users.first()
        
        if check_pw_hash(password, user.password):
            return JsonResponse({
                "success": True,
                "user":{
                    "id": user.id,
                    "phone": user.phone,
                    "role_id": user.role.id,
                    "role": user.role.name,
                    "password": user.password,
                },
            }) 
        return JsonResponse({"error": "Incorrect phone or password!"})        
    return JsonResponse({"error": request.method + " method not allowed!"})

@csrf_exempt
def book_time(request):
    if request.method == "POST":
        user_id = int(request.POST["user_id"])
        company_id = int(request.POST["company_id"])
        service_id = int(request.POST["service_id"])
        password = request.POST["password"]
        book_time = request.POST["book_time"]
        date_book_time = datetime.strptime(book_time, '%d-%m-%Y %H:%M')
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "Not authorized!"})
        if not check_pw_hash(password, user.password):
            return JsonResponse({"error": "Not authorized!"})
        
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return JsonResponse({"error": "Company not exist!"})

        services = company.services.all()
        service = None
        has_places = False
        for current_service in services:
            for day in current_service.days.all():
                if int(day.day) == date_book_time.weekday():
                    for timeline in day.timelines.all():
                        if timeline.start_time < date_book_time.time() and timeline.end_time > date_book_time.time():
                            has_places = True
                            service = current_service
                            break

        if not has_places:
            return JsonResponse({"error": "В это время по этой услуге заниматься нельзя!"})   
        
        timer = Timer.objects.create(user=user,company=company, service=service, end_time=date_book_time + timedelta(minutes=20), start_time=date_book_time)
        timer.save()
        download_thread = threading.Thread(target=timer.start_timer, name="start_timer" + str(timer.id))
        download_thread.start()
        broadcast_ticks({
            "new_book": True,
            "timer_id": timer.id,
            "timer_start": str(timer.start_time),
            "timer_end": str(timer.end_time),
            "timer_service": timer.service.name,
            "timer_user": timer.user.phone,
            "company_id": timer.company.id,
        })
        return JsonResponse({"success": "Company was booked!"})        
    return JsonResponse({"error": request.method + " method not allowed!"})

@csrf_exempt
def confirm_book(request):
    if request.method == "POST":
        user_id = int(request.POST["user_id"])
        company_id = int(request.POST["company_id"])
        password = request.POST["password"]
        current_time = request.POST["current_time"]
        date_current_time = datetime.strptime(current_time, '%d-%m-%Y %H:%M')
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "Not authorized!"})
        if not check_pw_hash(password, user.password):
            return JsonResponse({"error": "Not authorized!"})
        
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return JsonResponse({"error": "Company not exist!"})
        
        book_timers = Timer.objects.filter(user=user, company=company)
        book_timer = None
        for timer in book_timers:
            if(timer.start_time - timedelta(minutes=10) <= date_current_time and timer.end_time > date_current_time):
                book_timer = timer
                break
        
        if not book_timer:
            if(len(book_timers) > 0):
                return JsonResponse({"error": "Вы сможете подтвердить бронь только в " + str(book_timers[0].start_time - timedelta(minutes=10))})
            else:
                return JsonResponse({"error": "Бронь не найдена!"})
        elif     not book_timer.is_confirmed:
            return JsonResponse({"error": "Ваша бронь не подтверждена!"})
        else:
            timer = TrainTimer.objects.create(user=user,company=company, service=book_timer.service, start_time=date_current_time)
            timer.save()
            book_timer.end_timer()
            #book_timer.delete()
            
            download_thread = threading.Thread(target=timer.start_timer, name="start_train_timer"+ str(timer.id))
            download_thread.start()
            broadcast_ticks({
                "new_timer": True,
                "timer_id": timer.id,
                "timer_start": str(timer.start_time),
                "timer_service": timer.service.name,
                "timer_user": timer.user.phone,
                "company_id": timer.company.id,
            })
            return JsonResponse({"success": "Тренировка началась!"})        
    return JsonResponse({"error": request.method + " method not allowed!"})

@csrf_exempt
def accept_book(request): # Клуб принял бронь
    if request.method == "POST":
        timer_id = int(request.POST["timer_id"])
        timer = Timer.objects.filter(id=timer_id).first() 
        if not timer:
            return JsonResponse({"success": "Такой брони уже не существует!"})     
        timer.is_confirmed = True
        timer.save()
        broadcast_ticks({
            "company_id": timer.company.id,
            "accept_book": True,
            "service": timer.service.name,
            "start_time": str(timer.start_time),
            "end_time": str(timer.end_time),
            "user": timer.user.phone,
            "timer_id": timer_id,
        })
        return JsonResponse({"success": "Бронь подтверждена!"})        
    return JsonResponse({"error": request.method + " method not allowed!"})

@csrf_exempt
def decline_book(request): # Клуб отклонил бронь
    if request.method == "POST":
        timer_id = int(request.POST["timer_id"])
        timer = Timer.objects.filter(id=timer_id).first() 
        timer.delete()
        broadcast_ticks({
            "company_id": timer.company.id,
            "decline_book": True,
            "timer_id": timer_id,
        })
        return JsonResponse({"success": "Бронь подтверждена!"})        
    return JsonResponse({"error": request.method + " method not allowed!"})

@csrf_exempt
def end_train(request):
    if request.method == "POST":
        user_id = int(request.POST["user_id"])
        company_id = int(request.POST["company_id"])
        password = request.POST["password"]
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "Not authorized!"})
        if not check_pw_hash(password, user.password):
            return JsonResponse({"error": "Not authorized!"})
        
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return JsonResponse({"error": "Company not exist!"})
        
        train_timer = TrainTimer.objects.filter(user=user, company=company).first()
        finished_train = FinishedTrain.objects.create(start_time=train_timer.start_time, end_time=train_timer.end_time, user=user, company=company, service=train_timer.service, minutes=train_timer.minutes)
        train_timer.close_timer = True
        train_timer.save()
        price = train_timer.end_timer()
        finished_train.bill = price
        finished_train.save()
        broadcast_ticks({
            "new_history": True,
            "phone": finished_train.user.phone,
            "service": finished_train.service.name,
            "start_time": datetime.strptime(finished_train.start_time, '%d-%m-%Y %H:%M'),
            "end_time": datetime.strptime(finished_train.end_time, '%d-%m-%Y %H:%M'),
            "minutes": finished_train.minutes,
            "bill": finished_train.bill,
            "history_id": finished_train.id,
        })

        return JsonResponse({"success": "Тренировка окончена!", "bill": price})        
    return JsonResponse({"error": request.method + " method not allowed!"})

@csrf_exempt
def update_schedules(request):
    if request.method == "POST":
        schedules_json = request.POST["schedules"]
        schedules = json.loads(schedules_json)
        service_id = int(request.POST["service"])
        print(service_id)
        service = Service.objects.get(id=service_id)
        service.name = request.POST["name"]
        service.description = request.POST["description"]
        service.save()
        if not check_timelines(schedules):
            return JsonResponse({"error": "Нельзя накладывать время занятия друг на друга!"})
        for schedule in schedules:
            current_schedule = service.days.all().filter(day=schedule["day"]).first()
            for timeline in schedule["timelines"]:
                print(timeline)
                print(current_schedule.timelines.all())
                db_timeline = TimeLine.objects.filter(id=timeline["id"]).first()
                print(db_timeline)
                if db_timeline:
                    start_time = datetime.strptime(timeline["start_time"], '%H:%M')
                    end_time = datetime.strptime(timeline["end_time"], '%H:%M')
                    
                    db_timeline.price = timeline["price"]
                    db_timeline.start_time = start_time
                    db_timeline.end_time = end_time
                    db_timeline.limit_people = timeline["limit_people"]
                    db_timeline.save()
            current_schedule.save()
        return JsonResponse({"success": "NICE BOY!"})
         
    return JsonResponse({"error": request.method + " method not allowed!"})

@csrf_exempt
def add_timeline(request):
    if request.method == "POST":
        schedule_id = request.POST["schedule"]
        schedule = Schedule.objects.get(id=schedule_id)
        
        new_timeline = TimeLine.objects.create()
        schedule.timelines.add(new_timeline)
        schedule.save()
        print(str(new_timeline.start_time))
        return JsonResponse({"id": new_timeline.id, "start_time": str(new_timeline.start_time)[:-3], "end_time": str(new_timeline.end_time)[:-3], "limit_people": new_timeline.limit_people, "price": new_timeline.price})
    return JsonResponse({"error": request.method + " method not allowed!"})




@csrf_exempt
def add_image(request):
    if request.method == "POST":
        image = request.FILES["image"]
        service_id = request.POST["service"]
        if(check_image_type(image)):
            model_image = MyImage.objects.create(image=image)
            model_image.save()
            service = Service.objects.get(id=service_id)
            service.images.add(model_image)
            service.save()
            return JsonResponse({"image": model_image.image.url, "id": model_image.id})
        else:
            upload_error = "Выберите .jpg или .png формат!" 
            return JsonResponse({"error": upload_error})
         
    return JsonResponse({"error": request.method + " method not allowed!"})

@csrf_exempt
def add_service(request):
    if request.method == "POST":
        service_id = request.POST["service"]
        user = get_current_user(request)
        service = Service.objects.get(id=service_id)
        user.company.services.add(service)
        user.save()
        
        return JsonResponse({"success":True})
         
    return JsonResponse({"error": request.method + " method not allowed!"})
# @csrf_exempt
# def add_to_history(request):
#     if request.method == "POST":
        
        
#     return JsonResponse({"error": request.method + " method not allowed!"})


@receiver(pre_delete, sender=MyImage)
def item_delete(sender, instance, **kwargs):
    instance.image.delete(False)

# @receiver(pre_delete, sender=Document)
# def document_delete(sender, instance, **kwargs):
#     instance.image.delete(False)
