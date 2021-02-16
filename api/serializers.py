from .models import *
from rest_framework import serializers
from django.core.serializers import serialize
from django.core.files.base import ContentFile
import base64
import six
import uuid
from .modules.hashutils import make_pw_hash
from django.http import Http404, JsonResponse
import json


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

class RoleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Role
        fields = ("id", "name")


class UserSerializer(serializers.ModelSerializer):
    role = RoleField(many=False, read_only=False)
    class Meta:
        model = User
        fields = ("id", "password", "role", "phone")
    
    def create(self, validated_data):
        try:
            user = User.objects.filter(phone=validated_data["phone"]).first()
            if user:
                raise Exception
            
        except:
            raise serializers.ValidationError("User alredy exist")
        user = User.objects.create(
            role=validated_data['role'],
            phone=validated_data['phone'],
            password = make_pw_hash(validated_data['password'],
            )
        )
        #user.password = validated_data['password']
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

class ScheduleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Schedule
        fields = ("id", "start_time", "end_time", "day")


class ServiceField(serializers.RelatedField):
    queryset = Service.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return Service.objects.get(id=data)
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

class ServiceSerializer(serializers.ModelSerializer):    
    days = ScheduleField(many=True, read_only=False)
    class Meta:
        model = Service
        fields = ("id", "price", "name", "description", "days", "limit_people")
    
    def create(self, validated_data):   
        days_data = validated_data.pop('days')
        print(days_data)
        service = Service.objects.create(**validated_data)
        days_list = [] 
        for days_details in days_data:                    
            days_list.append(Product.objects.filter(id=days_details).first())
        service.days.add(*days_list)
        return service

class CompanySerializer(serializers.ModelSerializer):    
    owner = UserField(many=False, read_only=False)
    services = ServiceField(many=True, read_only=False)
    class Meta:
        model = Company
        fields = [ "id", "name", "owner", "address", "latitude", "longitude", "services"]


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