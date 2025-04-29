from django.urls import path
from . import views
from django.contrib.auth import views as log_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Register URL
     path('engineer/', views.enghome, name='enghome'),  # Engineer page
     path('deptLeader/', views.deptLeaderHome, name='deptLeaderHome'),  # Dept Leader page
 #path('SeniorManager/', views.SenManagerHome, name='SenManagerHome'),  # Senior manager page
    
    path('login/', auth_views.LoginView.as_view(template_name='health_check/login.html'),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='health_check/logout.html'), name='logout'),

    # Voting & history
    path('voting/', views.voting_page,  name='voting_page'),
    path('voting/choose_session/', views.choose_session, name='choose_session'),
    path('voting/choose_session/set/<int:session_id>/', views.set_session, name='set_session'),
    path('history/', views.all_history, name='all_history'),

    # Statistics
    path('statistics/', views.statistics, name='statistics'),

]
