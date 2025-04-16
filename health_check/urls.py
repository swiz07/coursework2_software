from django.urls import path
from . import views
from django.contrib.auth import views as log_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Register URL
    path('enghome/', views.enghome, name='enghome'),  # Engineer page
    path('deptLeader/', views.deptLeaderHome, name='deptLeaderHome'),  # Dept Leader page
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'),
]
