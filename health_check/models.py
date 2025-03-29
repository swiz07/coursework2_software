# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager,Group,Permission

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, username,fullname,address,phone_number):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            fullname=fullname,
            address=address,
            phone_number=phone_number,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


#Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(max_length=25)
    email=models.EmailField(max_length=254, unique=True)
    fullname=models.CharField(max_length=254, null=True, blank=True)
    address=models.TextField()
    phone_number=models.CharField(max_length=15)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups', 
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email
    
# class user_type(models.Model):
#     is_engineer = models.BooleanField(default=False)
#     is_senior_manager = models.BooleanField(default=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         if self.is_engineer == True:
#             return User.get_email(self.user) + " - is_student"   
#         else:
#             return User.get_email(self.user) + " - is_senior_manager"