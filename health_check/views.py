from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from .models import *

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        fullname = request.POST['name']
        password = request.POST['password']
        address = request.POST['address']
        phone_number = request.POST['phone']
        role_name = request.POST['role']
        username=request.POST['username']
        
        role=Role.objects.get(name=role_name)

        # Create the user with the role
        try :user = User.objects.create_user(
            email=email,
            fullname=fullname,
            password=password,
            address=address,
            phone_number=phone_number,
            role=role,
        ) 
        except IntegrityError:
             messages.error(request, "This email is already registered.")
             return redirect('register')
        
        
        user.set_password(password)
        user.save()

        # Log the user in after registration
        auth_login(request, user)

        # Redirect to the appropriate home page based on the role
        if role.is_engineer:
            return redirect('enghome')
        elif role.is_team_leader:
            return redirect('enghome')
        elif role.is_department_leader:
            return redirect('deptLeaderHome')
        elif role.is_senior_manager:
            return redirect('deptLeaderHome')

    return render(request, 'health_check/register.html')

def login_user(request):
    print("LOGIN VIEW HIT")
    if (request.method == 'POST'):
        email = request.POST.get('email') #Get email value from form
        password = request.POST.get('password') #Get password value from form
        
        user = authenticate(request, username=email, password=password)
        
            
        
        if user is not None:
            print(f"Login successful for user: {user.email}")  # Debugging line
            
            auth_login(request, user)
            type_obj = user.role
            if user.is_authenticated and type_obj.is_engineer:
                print(f"Redirecting user to the correct page based on role...")
                return redirect('enghome') #Go to engineer home
            elif user.is_authenticated and type_obj.is_team_leader:
                print("Login successful")
                return redirect('deptLeaderHome') 
            elif user.is_authenticated and type_obj.is_senior_manager:
                return redirect('deptLeaderHome') 
            elif user.is_authenticated and type_obj.is_department_leader:
                return redirect('enghome') 
        else:
             
            return redirect('health_check/login.html')

    return render(request, 'health_check/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


# Home page view
def home(request):
    return render(request, 'home.html')
 
def enghome(request):
    return render(request, 'enghome.html')


def deptLeaderHome(request):
    return render(request, 'DeptLeaderHome.html') 
