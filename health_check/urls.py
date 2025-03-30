from django.urls import path
from . import views
from django.contrib.auth import views as log_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Register URL
    path('enghome/', views.enghome, name='enghome'),  # Engineer page
    path('login/', log_views.LoginView.as_view(template_name='health_check/login.html'), name='login'), 
    path('logout/', log_views.LogoutView.as_view(template_name='health_check/logout.html'), name='logout'),
]
