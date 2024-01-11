from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name="logout"),
    path('editbio/', views.editbio, name="editbio"),
]