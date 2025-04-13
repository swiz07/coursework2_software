from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import User, Role, Department, Team 

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        fullname = request.POST['name']
        password = request.POST['password']
        address = request.POST['address']
        phone_number = request.POST['phone']
        role_name = request.POST['role']
        department_name=request.POST['department']
        team_name=request.POST['team']

        role=Role.objects.get(role_name=role_name)
        department=Department.objects.get(department_name=department_name)
        team=Team.objects.get(team_name=team_name)

        # Create the user with the role
        user = User.objects.create_user(
            email=email,
            fullname=fullname,
            password=password,
            address=address,
            phone_number=phone_number,
            role=role,
            department=department,
            team=team
        )

        # Log the user in after registration
        auth_login(request, user)

        # Redirect to the appropriate home page based on the role
        if role.is_engineer:
            return redirect('enghome')
        elif role.is_team_leader:
            return redirect('home_team_leader')
        elif role.is_department_leader:
            return redirect('home_department_leader')
        elif role.is_senior_manager:
            return redirect('home_senior_manager')

    return render(request, 'health_check/register.html')

def login_user(request):
    if (request.method == 'POST'):
        email = request.POST.get('email') #Get email value from form
        password = request.POST.get('password') #Get password value from form
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            type_obj = user.role
            if user.is_authenticated and type_obj.is_engineer:
                return redirect('enghome') #Go to engineer home
            elif user.is_authenticated and type_obj.is_team_leader:
                return redirect('home_team_leader') 
            elif user.is_authenticated and type_obj.is_senior_manager:
                return redirect('home_senior_manager') 
            elif user.is_authenticated and type_obj.is_department_leader:
                return redirect('home_department_leader') 
        else:
            return redirect('home')

    return render(request, 'home.html')
# Home page view
def home(request):
    return render(request, 'home.html')
 
def enghome(request):
    return render(request, 'enghome.html')