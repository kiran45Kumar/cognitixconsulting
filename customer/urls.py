from django.urls import path
from .views import signup,login,CreateUser,LoginCheck,index,ViewCustomer,UpdateUser,DeleteUser,ForgotPassword,UpdatePassword,reset_password
from .views import index2,logout

urlpatterns = [
    path('signup/',signup,name='signup'),
    path('',login,name='login'),
    path('create_user/',CreateUser.as_view(),name='create_user'),
    path('login_check/',LoginCheck.as_view(),name='login_check'),
    path("index/",index,name='index'),
    path('view_customer/', ViewCustomer.as_view(),name='view_customer'),
    path('update_user/', UpdateUser.as_view(),name='update_user'),
    path('delete_user/', DeleteUser.as_view(),name='delete_user'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    path('update_password/',UpdatePassword.as_view(),name='update_password'),
    path('reset_password/<int:cid>/',reset_password,name='reset_password'),
    path('index2/',index2, name='index2'),
    path('logout/',logout,name='logout')
]