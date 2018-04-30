from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

from recommender import views

urlpatterns = [
    path('', views.index, name='index'),
    path('compute', views.compute, name='compute'),
    path('recommend', views.recommend, name='recommend'),
]
