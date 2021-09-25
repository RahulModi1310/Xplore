from .views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/',signin,name="signin"),
    path('register/',register,name='register'),
    path('confirm/<token>',confirm,name='confirm'),
    path('home/',home,name='home'),
    path('interests/',interests,name='interests'),
    path('main/',main,name='main'),

]
