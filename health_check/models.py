# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager,Group,Permission

class UserManager(BaseUserManager):
    def _create_user(self, email, fullname, address, phone_number, password=None, is_staff=False, is_superuser=False, role=None, username=None, department=None, team=None):
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
            role=role,
            team=team
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, fullname, address, phone_number, password=None, role=None, **extra_fields):
        return self._create_user(email, fullname, address, phone_number, password, False, False, role, **extra_fields)

    def create_superuser(self, email, fullname, address, phone_number, password=None, role=None, **extra_fields):
        return self._create_user(email, fullname, address, phone_number, password, True, True, role, **extra_fields)
    
class Role(models.Model):
    name=models.CharField(max_length=50, unique=True, null=True, blank=True)
    is_engineer = models.BooleanField(default=False)
    is_senior_manager = models.BooleanField(default=False)
    is_team_leader=models.BooleanField(default=False)
    is_department_leader=models.BooleanField(default=False)
    role_name = models.CharField(max_length=20)

    def __str__(self):
        return self.role_name
    
#Create your models here.
class User(AbstractBaseUser , PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(max_length=254, null=True, blank=True)
    address = models.TextField()
    phone_number = models.IntegerField()
    is_staff = models.BooleanField(default=False) # for admin
    is_superuser = models.BooleanField(default=False)# for admin
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    team=models.ForeignKey('Team', on_delete=models.CASCADE, null=True, blank=True)
    Account_id=models.ForeignKey('Account', on_delete=models.SET_NULL, null=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

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
    password=models.CharField(max_length=30, unique=True, null=True, blank=True)
    account_update=models.DateField(auto_now=True)
    account_status=models.BooleanField(default=True)
    account_type=models.CharField(max_length=50) 

class Card(models.Model):
    card_id=models.AutoField(primary_key=True)
    card_name=models.TextField()
    card_green_vote=models.IntegerField(default=0, blank=True) #number of green votes
    card_red_vote=models.IntegerField(default=0, blank=True)
    card_yellow_vote=models.IntegerField(default=0, blank=True)
    card_descrip=models.TextField()
    card_progress=models.TextField(null=True, blank=True)
    colour_code=models.TextField(null=True, blank=True) #has values like red, green and yellow
    session_id=models.ForeignKey('Session',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.card_name
    
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    session_started=models.DateTimeField() #when it is created
    session_deleted=models.DateTimeField(blank=True) #when the session is deleted/ended
    session_status=models.TextField()
    team_id=models.ForeignKey('Team',on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Session {self.session_id}"

class Team(models.Model):
    team_id=models.AutoField(primary_key=True)
    team_name=models.TextField()
    created_at=models.DateTimeField() 
    department_id=models.ForeignKey('Department', on_delete=models.CASCADE) 


    def __str__(self):
        return self.team_name


class Department(models.Model):
    department_id=models.AutoField(primary_key=True)
    department_name=models.TextField()
    created_date=models.DateField()

    def __str__(self):
        return self.department_name

    
class Vote(models.Model):
    vote_id=models.AutoField(primary_key=True)
    vote_value=models.TextField()
    vote_opinion=models.TextField() #progress note
    card_id=models.ForeignKey('Card',on_delete=models.CASCADE)
    session_id=models.ForeignKey('Session', on_delete=models.CASCADE)
    user_id=models.ForeignKey('User', on_delete=models.CASCADE)

class Summary(models.Model):
    summary_id=models.AutoField(primary_key=True)
    overall_health_rating=models.TextField()
    health_start_date=models.DateField()
    health_end_date=models.DateField()
    progress_over_time=models.TextField()
    team_id=models.ForeignKey('Team', on_delete=models.CASCADE)
    card_id=models.ForeignKey('Card', on_delete=models.CASCADE)
    department_id=models.ForeignKey('Department', on_delete=models.CASCADE)
    