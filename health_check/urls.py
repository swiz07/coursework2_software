from django.urls import path
from . import views
from django.contrib.auth import views as log_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Register URL
    path('engineer/', views.enghome, name='enghome'),  # Engineer page
    path('teamLeader/', views.teamLeader, name='teamLeaderHome'),  # Engineer page
    path('deptLeader/', views.deptLeaderHome, name='deptLeaderHome'),  # Dept Leader page
    path('SeniorManager/', views.SenManagerHome, name='SenManagerHome'),
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'),
    path('profile/',   views.profile, name='profile'),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='health_check/password_change.html',success_url='/password_change/done/'),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='health_check/password_change_done.html'),name='password_change_done'),
]
