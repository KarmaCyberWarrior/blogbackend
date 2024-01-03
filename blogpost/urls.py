from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('tag-list/', views.tagList, name="tag-list"),
    path('tag-detail/<str:pk>/', views.tagDetail, name="tag-detail"),
    path('tag-create/', views.tagCreate, name="tag-create"),
    path('tag-update/<str:pk>/', views.tagUpdate, name="tag-update"),
    path('tag-delete/<str:pk>/', views.tagDelete, name="tag-delete"),
    path('post-list/', views.postList, name="post-list"),
    path('post-list-trend/', views.postListTrend, name="post-list-trend"),
    path('post-detail/<str:pk>/', views.postDetail, name="post-detail"),
    path('post-create/', views.postCreate, name="post-create"),
    path('post-update/<str:pk>/', views.postUpdate, name="post-update"),
    path('post-delete/<str:pk>/', views.postDelete, name="post-delete"),
    path('comment-list/<str:pk>/', views.commentList, name="comment-list"),
    path('comment-detail/<str:pk>/', views.commentDetail, name="comment-detail"),
    path('comment-create/', views.commentCreate, name="comment-create"),
    path('comment-delete/<str:pk>/', views.commentDelete, name="comment-delete"),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('section-list/<str:pk>/', views.sectionList, name="section-list"),
    path('section-create/', views.sectionCreate, name="section-create"),
    path('section-delete/<str:pk>/', views.sectionDelete, name="section-delete"),
    path('section-photo/<str:pk>/', views.sectionPhoto, name="section-photo"),
    path('post-photo/<str:pk>/', views.postPhoto, name="post-photo"),
    path('reply-list/<str:pk>/', views.replyList, name="reply-list"),
    path('profile-list/', views.profileList, name="profile-list"),
    path('reply-create/', views.replyCreate, name="reply-create"),
    path('reply-delete/<str:pk>/', views.replyDelete, name="reply-delete"),
]