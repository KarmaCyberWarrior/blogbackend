from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name="logout"),
    path('editbio/', views.editbio, name="editbio"),
    path('create-post/', views.createpost, name="create-post"),
    path('draft-posts/', views.draftedpost, name="draft-posts"),
    path('edit-post/<str:pk>', views.editpost, name="edit-post"),
    path('publish/<str:pk>', views.publishpost, name="publish"),
    path('delete/<str:pk>', views.deletepost, name="delete"),
    path('team/', views.manageteam, name="manage-team"),
    path('edit-member/<str:pk>', views.editteamMember, name="edit-member"),
    path('delete-member/<str:pk>', views.deletemember, name="delete-member"),
    path('add-member/', views.addteammember, name="add-member"),
    path('editname/', views.editname, name="editname"),
    path('update-dp/', views.changepfp, name="update-dp"),
]