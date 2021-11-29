from .models import *
from rest_framework import serializers
from django.core.serializers import serialize
from django.core.files.base import ContentFile
import base64
import six
import uuid
from .modules.hashutils import make_pw_hash
from .modules.functions import get_random_string
from django.http import Http404, JsonResponse
import json
from adminpanel.models import *


class RoleField(serializers.RelatedField):
    queryset = Role.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return Role.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class CityField(serializers.RelatedField):
    queryset = City.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return City.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class RoleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Role
        fields = ("id", "name")


class MyImageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = MyImage
        fields = ("id", "image")

    

class MyImageField(serializers.RelatedField):
    queryset = MyImage.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return MyImage.objects.get(id=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class FriendSerializer(serializers.ModelSerializer):
    role = RoleField(many=False, read_only=False)
    class Meta:
        model = User
        fields = ("id", "role", "phone", "avatar", "ref_code", "bonuses", "trains_count", "avarage_train_time", "max_train_time", "most_visited_club")

class TelegramFriendSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ("id", "name", "phone", "telegram_id", "points", "ref_code")

class UserSerializer(serializers.ModelSerializer):
    role = RoleField(many=False, read_only=False, required=False)
    city = CityField(many=False, read_only=False, required=False)
    friends = FriendSerializer(many=True, read_only=False, required=False)
    telegram_friends = TelegramFriendSerializer(many=True, read_only=False, required=False)
    class Meta:
        model = User
        fields = ("id", "city", "role", "sex", "phone", "email", "avatar", "name", "second_name", "ref_code", "bonuses", "telegram_id", "points", "trains_count", "avarage_train_time", "max_train_time", "most_visited_club", "telegram_friends", "friends", "is_currently_training", "current_train")
    
    def create(self, validated_data):        
        try:
            user = User.objects.get(phone=validated_data["phone"])     
            raise serializers.ValidationError("User alredy exist")                 
        except:
            pass
        role = None
        name = None
        sex = None
        telegram_id = None
        try:
            role = validated_data['role']
        except:
            pass
        try:
            name = validated_data['name']
        except:
            pass
        try:
            sex = validated_data['sex']
        except:
            pass
        try:
            telegram_id = validated_data['telegram_id']
        except:
            pass
        user = User.objects.create(
            phone=validated_data['phone'],
        )
        user.generate_ref_code()
        if role:
            user.role = role
        if name:
            user.name = name
        if sex:
            user.sex = sex
        if telegram_id:
            user.telegram_id = int(telegram_id)
        user.save()
        return user


 
class UserField(serializers.RelatedField):    
    queryset = User.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return User.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )




class ScheduleField(serializers.RelatedField):
    queryset = Schedule.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return Schedule.objects.get(id=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class TimeLineSerializer(serializers.ModelSerializer):     
    class Meta:
        model = TimeLine
        fields = ("id", "price", "start_time", "end_time", "limit_people", "free_places")

class ScheduleSerializer(serializers.ModelSerializer):    
    #timelines = TimeLineSerializer(many=True, read_only=False, required=False)
    timelines = serializers.SerializerMethodField("get_timelines")

    def get_timelines(self, instance):        
        timelines = instance.timelines.all().order_by("start_time")
        return TimeLineSerializer(timelines, many=True, read_only=-False, required=False).data

    class Meta:
        model = Schedule
        fields = ("id", "day", "get_cutted_name", "get_fullname", "timelines")


# class ServiceField(serializers.RelatedField):
#     queryset = Service.objects.all()
#     def to_representation(self, value):
#         return value.id
#     def to_internal_value(self, data):
#         try:
#             try:
#                 return Service.objects.get(id=data)
#             except KeyError:
#                 raise serializers.ValidationError(
#                     'id is a required field.'
#                 )
#             except ValueError:
#                 raise serializers.ValidationError(
#                     'id must be an integer.'
#                 )
#         except Type.DoesNotExist:
#             raise serializers.ValidationError(
#             'Obj does not exist.'
#             )

class ServiceCategoryField(serializers.RelatedField):
    queryset = ServiceCategory.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return ServiceCategory.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class ServiceCategorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = ServiceCategory
        fields = ("id", "name", "image", "count_trains")

# class ServiceSerializer(serializers.ModelSerializer):    
#     #days = ScheduleSerializer(many=True, read_only=False, required=False, )
#     days = serializers.SerializerMethodField("get_days")
#     images = MyImageSerializer(many=True, read_only=False, required=False)
#     category = ServiceCategoryField(many=False, read_only=False, required=False)

#     def get_days(self, instance):
#         days = instance.days.all().order_by("day")
#         return ScheduleSerializer(days, many=True, read_only=-False, required=False).data

#     class Meta:
#         model = Service
#         fields = ("id", "category", "description", "days", "images")
    
#     def create(self, validated_data):   
#         service = Service.objects.create(**validated_data)
#         days_list = [] 
#         for count in range(0,7):                    
#             days_list.append(Schedule.objects.create(day=count))
#         service.days.add(*days_list)
#         return service

class CompanySerializer(serializers.ModelSerializer):    
    owner = UserSerializer(many=False, read_only=True, required=False)
    #services = ServiceSerializer(many=True, read_only=False, required=False)
    days = serializers.SerializerMethodField("get_days")
    images = MyImageSerializer(many=True, read_only=False, required=False)
    tags = ServiceCategorySerializer(many=True, read_only=False, required=False)
    class Meta:
        model = Company
        fields = [ "id", "name", "owner", "address", "latitude", "longitude", "qr_url", "description", "days", "images", "avatar", "tags", "all_bonuses", "avarage_price", "rating", "contacts"]

    def get_days(self, instance):
        days = instance.days.all().order_by("day")
        return ScheduleSerializer(days, many=True, read_only=-False, required=False).data

    def create(self, validated_data):
        owner = None
        address = None
        latitude = None
        longitude = None
        try:
            owner = validated_data['owner']
        except:
            pass
        try:
            address = validated_data['address']
        except:
            pass
        try:
            latitude = validated_data['latitude']
        except:
            pass
        try:
            longitude = validated_data['longitude']
        except:
            pass
        company = Company.objects.create(
            name=validated_data['name'],
            )
        try:
            tags = validated_data['tags']
            company.tags.set(tags)
        except:
            pass
            
        company.qr_url = qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + str(company.id)

        days_list = [] 
        for count in range(0,7):                    
            days_list.append(Schedule.objects.create(day=count))
        company.days.add(*days_list)

        if address:
            company.address = address
        if owner:
            company.owner = owner
        if latitude:
            company.latitude = latitude
        if longitude:
            company.longitude = longitude

        company.save()
    
        return company



class CompanyField(serializers.RelatedField):
    queryset = Company.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return Company.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class AdminUserSerializer(serializers.ModelSerializer):
    company = CompanyField(many=False, read_only=False)
    class Meta:
        model = AdminUser
        fields = ("id", "company", "username", "password")

class FinishedTrainSerializer(serializers.ModelSerializer):    
    user = UserField(many=False, read_only=False)
    #service = ServiceField(many=False, read_only=False)
    company = CompanyField(many=False, read_only=False)
    class Meta:
        model = FinishedTrain
        fields = ("id", "user", "company", "minutes", "start_time", "end_time", "bill")

class TimerSerializer(serializers.ModelSerializer):    
    user = UserSerializer(many=False, read_only=False)
    #service = ServiceField(many=False, read_only=False)
    company = CompanySerializer(many=False, read_only=False)
    class Meta:
        model = Timer
        fields = ("id", "user", "company", "start_time", "end_time", "is_paid", "price", "day", "book_date")

class TrainTimerSerializer(serializers.ModelSerializer):    
    user = UserField(many=False, read_only=False)
    #service = ServiceField(many=False, read_only=False)
    company = CompanyField(many=False, read_only=False)
    class Meta:
        model = TrainTimer
        fields = ("id", "user", "company", "start_time", "end_time", "minutes", "transaction_id")