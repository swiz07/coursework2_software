from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
)


class Role(models.Model):
    name                  = models.CharField(max_length=50, unique=True, null=True, blank=True)
    is_engineer           = models.BooleanField(default=False)
    is_team_leader        = models.BooleanField(default=False)
    is_department_leader  = models.BooleanField(default=False)
    is_senior_manager     = models.BooleanField(default=False)
    role_name             = models.CharField(max_length=20)

    def __str__(self):
        return self.role_name


class Account(models.Model):
    account_id      = models.AutoField(primary_key=True)
    username        = models.CharField(max_length=20, unique=True)
    password        = models.CharField(max_length=128)  
    account_update  = models.DateField(auto_now=True)
    account_status  = models.BooleanField(default=True)
    account_type    = models.CharField(max_length=50)

    def __str__(self):
        return self.username



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
            team=team,
            department=department
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, fullname, address, phone_number, password=None, role=None, **extra_fields):
        return self._create_user(email, fullname, address, phone_number, password, False, False, role, **extra_fields)

    def create_superuser(self, email, fullname, address, phone_number, password=None, role=None, **extra_fields):
        return self._create_user(email, fullname, address, phone_number, password, True, True, role, **extra_fields)
    


class User(AbstractBaseUser, PermissionsMixin):
    user_id      = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25, unique=True)
    email        = models.EmailField(max_length=254, unique=True)
    fullname     = models.CharField(max_length=254, blank=True)
    address      = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    role         = models.ForeignKey(Role,         on_delete=models.CASCADE, null=True, blank=True)
    department   = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    team         = models.ForeignKey('Team',       on_delete=models.CASCADE, null=True, blank=True)
    Account_id   = models.ForeignKey(Account,      on_delete=models.SET_NULL, null=True, blank=True)

    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups           = models.ManyToManyField(Group,      related_name='custom_user_groups',      blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'fullname', 'address', 'phone_number']

    objects = UserManager()

    def __str__(self):
        team_part = self.team.team_name if self.team else "No Team"
        return f"{self.email} ({team_part})"



#Departments & Teams

class Department(models.Model):
    department_id   = models.AutoField(primary_key=True)
    department_name = models.TextField()
    created_date    = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['department_name']

    def __str__(self):
        return self.department_name


class Team(models.Model):
    team_id       = models.AutoField(primary_key=True)
    team_name     = models.TextField()
    created_at    = models.DateTimeField(auto_now_add=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        ordering = ['team_name']

    def __str__(self):
        return f"{self.team_name} – {self.department_id.department_name}"



#Sessions (cards belong to a session)

class Session(models.Model):
    session_id      = models.AutoField(primary_key=True)
    session_name    = models.TextField()
    session_started = models.DateTimeField()
    session_deleted = models.DateTimeField(null=True, blank=True)
    session_status  = models.TextField()
    team_id         = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-session_started']

    def __str__(self):
        return f"{self.team_id.team_name} – {self.session_name}"



# Cards with aggregators + description + progress

class Card(models.Model):
    card_id          = models.AutoField(primary_key=True)
    card_name        = models.TextField()
    card_descrip     = models.TextField(blank=True)
    card_progress    = models.TextField(blank=True)
    colour_code      = models.TextField(blank=True)

    session_id       = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    card_red_vote    = models.IntegerField(default=0, blank=True)
    card_yellow_vote = models.IntegerField(default=0, blank=True)
    card_green_vote  = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.card_name



#Votes 

class Vote(models.Model):
    vote_id      = models.AutoField(primary_key=True)
    vote_value   = models.CharField(max_length=20)  # green/amber/red
    vote_opinion = models.TextField()               # progress note

    card_id      = models.ForeignKey(Card,    on_delete=models.CASCADE)
    session_id   = models.ForeignKey(Session, on_delete=models.CASCADE)
    user_id      = models.ForeignKey(User,    on_delete=models.CASCADE)

    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_id.email} → {self.card_id.card_name} [{self.vote_value}/{self.vote_opinion}]"



#Summary 

class Summary(models.Model):
    summary_id             = models.AutoField(primary_key=True)
    overall_health_rating  = models.TextField()
    health_start_date      = models.DateField()
    health_end_date        = models.DateField()
    progress_over_time     = models.TextField()
    team_id                = models.ForeignKey(Team,       on_delete=models.CASCADE)
    card_id                = models.ForeignKey(Card,       on_delete=models.CASCADE)
    department_id          = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.team_id.team_name} – {self.card_id.card_name} summary"
