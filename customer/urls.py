from django.urls import path
from .views import signup,login,CreateUser,LoginCheck,index
urlpatterns = [
    path('signup/',signup,name='signup'),
    path('login/',login,name='login'),
    path('create_user/',CreateUser.as_view(),name='create_user'),
    path('login_check/',LoginCheck.as_view(),name='login_check'),
    path("index/",index,name='index')
]