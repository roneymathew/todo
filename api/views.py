from rest_framework import viewsets, status,filters
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .serializers import *
from .models import *

from rest_framework.decorators import api_view,permission_classes,renderer_classes
from rest_framework import permissions
from rest_framework.renderers import BaseRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import uuid
import datetime
import os
User = get_user_model()


from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_admin(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get('username',None):
                if request.data.get('password',None) and request.data.get('password1') and request.data.get('password') == request.data.get('password1'):
                    if not User.objects.filter(username = request.data['username']).exists():
                        user = User( user_type = 'AD',username = request.data['username'])
                        user.set_password(request.data['password'])
                        if request.data.get('first_name',None):
                            user.first_name = request.data['first_name']
                        if request.data.get('last_name',None):
                            user.last_name = request.data['last_name']
                        if request.data.get('email',None):
                            user.email = request.data['email']
                        user.save()
                    else:
                        return Response('Username already exists',status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Check your password" , status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Provide a username" , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied" , status = status.HTTP_400_BAD_REQUEST)
    return Response("all set",status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get('username',None):
                if request.data.get('password',None) and request.data.get('password1') and request.data.get('password') == request.data.get('password1'):
                    if not User.objects.filter(username = request.data['username']).exists():
                        user = User( user_type = 'US',username = request.data['username'])
                        user.set_password(request.data['password'])
                        if request.data.get('first_name',None):
                            user.first_name = request.data['first_name']
                        if request.data.get('last_name',None):
                            user.last_name = request.data['last_name']
                        if request.data.get('email',None):
                            user.email = request.data['email']
                        user.save()
                    else:
                        return Response('Username already exists',status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Check your password" , status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Provide a username" , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied" , status = status.HTTP_400_BAD_REQUEST)
    return Response("all set",status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_catagory(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get('name',None):
                if not Category.objects.filter(name = request.data['name']).exists():
                    category = Category( user_type = 'US')
                    if request.data.get('colour_code',None):
                        category.colour_code = request.data['colour_code']
                    category.save()
                else:
                    return Response('name already exists',status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Provide a name" , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied" , status = status.HTTP_400_BAD_REQUEST)
    return Response("all set",status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Editcatagory(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get("catagory_id",None):
                if Category.objects.filter(id = request.data["catagory_id"]).exists():
                    category = Category.objects.filter(id = request.data["catagory_id"])[0]
                    if request.data.get(',name',None):
                        category.name = request.data["name"]
                    if request.data.get('colour_code',None):
                        categorycolour_code = request.data["colour_code"]
                    category.save()      
                    return Response("category updated",status = status.HTTP_200_OK)
                else:
                    return Response('Invalid category id',status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Must provide category id',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Permission denied',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Methord not accepted',status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Deletecatagory(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get("catagory_id",None):
                if Category.objects.filter(id = request.data["catagory_id"]).exists():
                    category = Category.objects.filter(id = request.data["catagory_id"]).delete()
                    return Response("category deleted",status = status.HTTP_200_OK)
                else:
                    return Response('Invalid category id',status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Must provide category id',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Permission denied',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Methord not accepted',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def catagoryList(request):
    queryset = Category.objects.all()
    filter_search = request.query_params.get('search', None)
    order_by = request.query_params.get('ordering',None)
    if order_by:
        queryset = queryset.order_by(order_by)
    if filter_search:
        queryset = queryset.filter( Q(name__contains  = filter_search) )
    data = queryset.values('id','name','colour_code')
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_todotask(request):
    if request.method == 'POST':
        if request.user.user_type == 'US':
            if request.data.get("title",None) and request.data.get("description",None):
                to_do_obj = ToDoDetails.objects.create(title = request.data["title"],description = request.data["description"],createdby = request.user)
                if request.data.get('note',None):
                    to_do_obj.note = request.data['note']
                if request.data.get('end_time',None):
                    to_do_obj.end_time = request.data['end_time']
                if request.data.get('priority',None):
                    if request.data['priority'] in [1,2,3,4]:
                        to_do_obj.priority = request.data['priority']
                to_do_obj.save()      
                return Response('Task created', status = status.HTTP_200_OK)
            else:
                return Response('Must provide title and description',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Permission denied',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Methord not accepted',status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Edittodotask(request):
    if request.method == 'POST':
        if request.user.user_type == 'US':
            if request.data.get("task_id",None):
                if ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user).exists():
                    to_do_obj = ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user)[0]
                    if request.data.get('title',None):
                        to_do_obj.title = request.data["title"]
                    if request.data.get('description',None):
                        to_do_objdescription = request.data["description"]
                    if request.data.get('note',None):
                        to_do_obj.note = request.data['note']
                    if request.data.get('end_time',None):
                        to_do_obj.end_time = request.data['end_time']
                    if request.data.get('priority',None):
                        if request.data['priority'] in [1,2,3,4]:
                            to_do_obj.priority = request.data['priority']
                    to_do_obj.save()      
                    return Response("Task updated",status = status.HTTP_200_OK)
                else:
                    return Response('Invalid Task id',status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Must provide task id',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Permission denied',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Methord not accepted',status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_catagory_to_todo(request):
    if request.method == 'POST':
        if request.user.user_type == 'US':
            if request.data.get("catagory_id",None) and request.data.get("task_id",None):
                if ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user).exists() and Category.objects.filter(id__in = request.data["catagory_id"]).exists():
                    todo_obj = ToDoDetails.objects.filter(id = request.data["task_id"])[0]
                    category = Category.objects.filter(id__in = request.data["catagory_id"])
                    if not Categorize.objects.filter(category = category,todo = todo_obj).exists():
                        categorize_objects = Categorize.objects.create(category = category,todo = todo_obj)
                        return Response("Task added to catagory",status = status.HTTP_200_OK)
                    else:
                        return Response('Task already added', status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response('Provide valid ids', status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Must provide catagory and task ids',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Permission denied',status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_catagory_to_todo(request):
    if request.method == 'POST':
        if request.user.user_type == 'US':
            if request.data.get("catagory_id",None) and request.data.get("task_id",None):
                if ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user).exists() and Category.objects.filter(id__in = request.data["catagory_id"]).exists():
                    todo_obj = ToDoDetails.objects.filter(id = request.data["task_id"])[0]
                    category = Category.objects.filter(id__in = request.data["catagory_id"])
                    if Categorize.objects.filter(category = category,todo = todo_obj).exists():
                        categorize_objects = Categorize.objects.filter(category = category,todo = todo_obj).delete()
                        return Response("Task removed from catagory",status = status.HTTP_200_OK)
                    else:
                        return Response('Task not belong to catagory', status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response('Provide valid ids', status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Must provide catagory and task ids',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Permission denied',status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DeleteToDo(request):
    if request.user.user_type == 'US':
        if request.data.get("task_id",None):
            if ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user).exists():
                to_do_obj = ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user).delete()
                return Response("Task deleteed",status = status.HTTP_200_OK)
            else:
                return Response("permission denied",status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Must provide Task id',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response("permission denied",status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ToDoList(request):
    if request.user.user_type == 'US':
        queryset = ToDoDetails.objects.filter(createdby = request.user)
    else:
        return Response('Permission denied',status = status.HTTP_400_BAD_REQUEST)
    filter_search = request.query_params.get('search', None)
    order_by = request.query_params.get('ordering',None)
    task_id = request.query_params.get('taskid',None)
    if task_id:
        queryset = queryset.filter(id = task_id)
    if order_by:
        queryset = queryset.order_by(order_by)
    if filter_search:
        queryset = queryset.filter( Q(title__contains  = filter_search) | Q (description__contains = filter_search))
    data = queryset.values('id','title','description','createdby','createdtme','last_updated','end_time','note','status','priority')
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserList(request):
    queryset = User.objects.filter(user_type = 'US')
    filter_search = request.query_params.get('search', None)
    order_by = request.query_params.get('ordering',None)
    user_id = request.query_params.get('userid',None)
    if user_id:
        queryset = queryset.filter(id = user_id)
    if order_by:
        queryset = queryset.order_by(order_by)
    if filter_search:
        queryset = queryset.filter( Q(email__contains  = filter_search) | Q (username__contains = filter_search) | Q (first_name__contains = filter_search))
    data = queryset.values('id','first_name','last_name','email','user_type')
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ShareToDo(request):
    if request.user.user_type == 'US':
        if request.data.get("task_id",None) and request.data.get("share_id",None):
            if ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user).exists() and User.objects.filter(id = request.data['share_id'],user_type = 'US').exists():
                to_do_obj = ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user)[0]
                user_obj = User.objects.filter(id = request.data['share_id'],user_type = 'US')[0]
                share_obj = ShareToDO.objects.create(todo = to_do_obj,user = user_obj)
                return Response("Task shared",status = status.HTTP_200_OK)
            else:
                return Response("permission denied",status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Must provide Task id and user to share',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response("permission denied",status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def MarkAsComplete(request):
    if request.method == 'POST':
        if request.user.user_type == 'US':
            if request.data.get("task_id",None):
                if ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user).exists():
                    to_do_obj = ToDoDetails.objects.filter(id = request.data["task_id"] , createdby = request.user)[0]
                    to_do_obj.status = 3
                    to_do_obj.save()      
                    return Response("Task completed",status = status.HTTP_200_OK)
                else:
                    return Response('Invalid Task id',status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Must provide task id',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Permission denied',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Methord not accepted',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sharedToDoList(request):
    if request.user.user_type == 'US':
        queryset = ToDoDetails.objects.filter(sharetodo__user = request.user)
    else:
        return Response('Permission denied',status = status.HTTP_400_BAD_REQUEST)
    filter_search = request.query_params.get('search', None)
    order_by = request.query_params.get('ordering',None)
    task_id = request.query_params.get('taskid',None)
    if task_id:
        queryset = queryset.filter(id = task_id)
    if order_by:
        queryset = queryset.order_by(order_by)
    if filter_search:
        queryset = queryset.filter( Q(title__contains  = filter_search) | Q (description__contains = filter_search))
    data = queryset.values('id','title','description','createdby','createdtme','last_updated','end_time','note','status','priority')
    return Response(data)