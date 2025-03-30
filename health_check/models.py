# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager,Group,Permission
from django.contrib.auth.models import User

class UserManager(BaseUserManager):
    def _create_user(self, email, fullname, address, phone_number, password=None, is_staff=False, is_superuser=False, role=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            fullname=fullname,
            address=address,
            phone_number=phone_number,
            is_staff=is_staff,
            is_superuser=is_superuser,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, fullname, address, phone_number, password=None, role=None, **extra_fields):
        return self._create_user(email, fullname, address, phone_number, password, False, False, role, **extra_fields)

    def create_superuser(self, email, fullname, address, phone_number, password=None, role=None, **extra_fields):
        return self._create_user(email, fullname, address, phone_number, password, True, True, role, **extra_fields)
    
class Role(models.Model):
    is_engineer = models.BooleanField(default=False)
    is_senior_manager = models.BooleanField(default=False)
    role_name = models.CharField(max_length=20)

    def __str__(self):
        return self.role_name

    def __str__(self):
        return self.role_name
    
#Create your models here.
class User(AbstractBaseUser , PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(max_length=254, null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey(Role, related_name='users', on_delete=models.CASCADE)

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    USERNAME_FIELD = 'email'  # Use email as the username field
    REQUIRED_FIELDS = ['fullname', 'address', 'phone_number']  # Required fields for createsuperuser

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def get_email(self):
        return self.email


class Account(models.Model):
    account_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=20, unique=True)
    account_update=models.DateField(auto_now=True)
    account_status=models.BooleanField(default=True)
    account_type=models.CharField(max_length=50) 

