from django.urls import path,include
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter(trailing_slash=True)


urlpatterns = [
    url('', include(router.urls)),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url('createadmin/',views.create_admin),
    url('createuser/',views.create_user),
    url('create_todo/',views.create_todotask),
    url('edit_todo/',views.Edittodotask),
    url('add_catagory_to_todo/',views.add_catagory_to_todo),
    url('remove_catagory_to_todo/',views.remove_catagory_to_todo),
    url('deleteToDo/',views.DeleteToDo),
    url('todolist',views.ToDoList),
    url('userlist/',views.UserList),
    url('shareto',views.ShareToDo),
    url('createcatagory/',views.create_catagory),
    url('editcatagory',views.Editcatagory),
    url('deletecatagory/',views.Deletecatagory),
    url('catagoryList',views.catagoryList),
    url('sharedtodolist',views.sharedToDoList),
    ]