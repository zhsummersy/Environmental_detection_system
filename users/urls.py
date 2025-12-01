from django.urls import path
from users import views

urlpatterns = [
    path("", views.index,name='index'),
    path("fan", views.fan,name='fan'),
    path("warn", views.warn,name='warn'),
    path('login', views.login,name='login'),
    path('register',views.register,name='register'),
    path('userpage', views.userpage,name='userpage'),
    path('chart', views.chart,name='chart'),
    path('table', views.table,name='table'),
    path('outlogin', views.outlogin,name='outlogin'),
    path('register/',views.register,name='register'),
    path('upload', views.upload, name='upload'),
    path('getMax', views.getMax, name='getMax'),
    path('alert', views.alert, name='alert'),
    path('FanZT', views.FanZT, name='FanZT'),
    path('FanStart', views.FanStart, name='FanStart'),
    path('FanStop', views.FanStop, name='FanStop'),


]
