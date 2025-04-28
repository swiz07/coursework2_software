from django.urls import path
from . import views
from django.contrib.auth import views as log_views 
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),  # Home page
    # Register URL
    path('register/', views.register, name='register'),  
   path('ajax/load-teams/', views.load_teams, name='ajax_load_teams'),



    # Home pages
    path('engineer/', views.enghome, name='enghome'),  # Engineer page
    path('teamLeaderHome/', views.teamLeader, name='teamLeaderHome'),  # Engineer page
    path('deptLeaderHome/', views.deptLeaderHome, name='deptLeaderHome'),  # Dept Leader page
    path('SenManagerHome/', views.SenManagerHome, name='SenManagerHome'), # Senior manager

    # Log in and log oout
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/',   views.profile, name='profile'),

    # Change password
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='health_check/password_change.html',success_url='/password_change/done/'),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='health_check/password_change_done.html'),name='password_change_done'),
] 