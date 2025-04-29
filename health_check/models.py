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
        extra_fields.setdefault('username', 'admin')
        extra_fields.setdefault('fullname', 'Admin User')
        extra_fields.setdefault('address', 'Admin Address')
        extra_fields.setdefault('phone_number', '0000000000')

        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


ROLE_CHOICES = [
    ('engineer', 'Engineer'),
    ('team_leader', 'Team Leader'),
    ('dept_leader', 'Department Leader'),
    ('senior_manager', 'Senior Manager'),
]


class Department(models.Model):
    """
    A real table instead of the plain CharField we were storing on Team.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Team(models.Model):
    name       = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="teams",
    )

    class Meta:
        unique_together = ("name", "department")
        ordering        = ["department__name", "name"]

    def __str__(self):
        return f"{self.department.name} – {self.name}"


#Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True)
    email=models.EmailField(max_length=254, unique=True)
    fullname=models.CharField(max_length=254, null=True, blank=True)
    address=models.TextField()
    phone_number=models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='engineer')
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True)

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
    REQUIRED_FIELDS = ['email', 'fullname', 'address', 'phone_number']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email
    
    def __str__(self):
        if self.team:
            return f"{self.team.department.name} – {self.team.name} ({self.username})"
        return f"{self.username} (No Team Assigned)"
    
# class user_type(models.Model):
#     is_engineer = models.BooleanField(default=False)
#     is_senior_manager = models.BooleanField(default=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         if self.is_engineer == True:
#             return User.get_email(self.user) + " - is_student"   
#         else:
#             return User.get_email(self.user) + " - is_senior_manager"




class Session(models.Model):
    date       = models.DateTimeField(help_text="When the session happens")
    created_on = models.DateField(auto_now_add=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status     = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.pk} – {self.date.strftime('%d/%m/%Y %I:%M %p')} ({self.get_status_display()})"
    

class Card(models.Model):
    """
    Represents a 'health check' card that users can vote on.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    # aggregator fields
    red_votes = models.PositiveIntegerField(default=0)
    yellow_votes = models.PositiveIntegerField(default=0)
    green_votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Vote(models.Model):
    VOTE_CHOICES = [
        ('red',    'Unsatisfied'),
        ('yellow', 'Partially Satisfied'),
        ('green',  'Satisfied'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    user        = models.ForeignKey(User,    on_delete=models.CASCADE)
    card        = models.ForeignKey(Card,    on_delete=models.CASCADE)
    vote_choice = models.CharField(max_length=10, choices=VOTE_CHOICES)
    reason      = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.card.title} [{self.vote_choice}]"


