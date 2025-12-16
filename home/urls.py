from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # USER
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('essay/', views.essay_view, name='essay'),
    path('submit/', views.submit_essay, name='submit_essay'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    # CUSTOM ADMIN DASHBOARD
    path(
    'dashboard/user/<int:user_id>/delete/',
    views.delete_user,
    name='delete_user'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/essay/<int:essay_id>/approve/', views.approve_essay, name='approve_essay'),
    path('dashboard/essay/<int:essay_id>/reject/', views.reject_essay, name='reject_essay'),
    path('dashboard/essay/<int:essay_id>/delete/', views.delete_essay, name='delete_essay'),

    # DEFAULT DJANGO ADMIN
    path('admin/', admin.site.urls),
]
