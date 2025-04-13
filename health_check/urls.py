from django.urls import path
from . import views
from django.contrib.auth import views as log_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Register URL
    path('engineer/', views.enghome, name='enghome'),  # Engineer page
    path('teamLeader/', views.teamLeader, name='teamLeaderHome'),  # Engineer page
    path('deptLeader/', views.deptLeaderHome, name='deptLeaderHome'),  # Dept Leader page
    path('SeniorManager/', views.SenManagerHome, name='SenManagerHome'),  # Senior manager page
    path('login/', log_views.LoginView.as_view(template_name='health_check/login.html'), name='login'), 
    path('logout/', log_views.LogoutView.as_view(template_name='health_check/logout.html'), name='logout'),
]
