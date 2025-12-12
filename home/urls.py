from django.urls import path
from django.http import HttpResponse
from .import views 

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('home/', views.login_view, name='login'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('essay/', views.essay_view, name='essay'),
    path('submit/', views.submit_essay, name='submit_essay'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]