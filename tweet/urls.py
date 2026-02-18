from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('add_review/', views.add_review, name='add_review'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('register/', views.register, name='register'),
    path('like_count/<int:pk>/', views.like_count, name='like_count'),
    path('tweet/<int:tweet_id>/comment/', views.add_comment, name='add_comment'),
    path('profile/', views.profile, name='profile'),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/<str:username>/", views.profile_user, name="user_profile"),
    path("profile/<str:username>/follow/", views.follow_toggle, name="follow_toggle"),
   

]
