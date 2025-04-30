#
    #File Name: admin.py
    #Author: Swizel De Melon
    #Co-Authors: none
#} 
from django.apps import AppConfig


class HealthCheckConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'health_check'
