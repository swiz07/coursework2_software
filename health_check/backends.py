# Title: Django Email Login (instead of using username)
# Author: Adi Ramadhan
# Date:26th August 2023
# AVailability: https://adiramadhan17.medium.com/django-email-login-instead-using-username-7377d3357257
 

from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
