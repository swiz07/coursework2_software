from django.shortcuts import render, redirect
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required


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
        user = User.objects.create_user(
            email=email, 
            fullname=fullname,
            password=password,
            address=address,
            phone_number=phone_number,
            role=role,
        ) 
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.set_password(password)
        user.save()

        # Log the user in after registration
        auth_login(request, user)

        # Redirect to the appropriate home page based on the role
        if role.is_engineer:
            return redirect('enghome')
        elif role.is_team_leader:
            return redirect('teamLeaderHome')
        elif role.is_department_leader:
            return redirect('deptLeaderHome')
        elif role.is_senior_manager:
            return redirect('SenManagerHome')

    return render(request, 'health_check/register.html')

def login_user(request):
    print("LOGIN VIEW HIT")
    if (request.method == 'POST'):
        email = request.POST.get('email')   
        password = request.POST['password']
        print(f"Attempting to authenticate with email: {email} and password: {password}")

        
        user = authenticate(request, email=email, password=password)
        
            
        
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
             
            return render(request, 'health_check/login.html' )


    return render(request, 'health_check/login.html')
 
 
#Logout page view
def logout_user(request):
    logout(request)
    return redirect('home')

# Home page view
def home(request):
    return render(request, 'home.html')

#Engineer page view
def enghome(request):
    return render(request, 'enghome.html')

def teamLeader(request):
    return render(request, 'teamLeaderHome.html')

def deptLeaderHome(request):
    return render(request, 'DeptLeaderHome.html') 


def SenManagerHome(request):
    return render(request, 'SenManagerHome.html')



def profile(request):
    # 1) Redirect any anonymous user to your login
    if not request.user.is_authenticated:
        return redirect('login')

    # 2) Safe to grab `request.user` fields now
    user = request.user

    # 3) Pull related names, guarding against None
    role_name  = user.role.role_name                        if user.role else ''
    team_name  = user.team.team_name                        if getattr(user, 'team', None) else ''
    account_id = user.Account_id.username                   if getattr(user, 'Account_id', None) else ''
        

    # 4) Build your context dict
    context = {
        'fullname':     user.fullname,
        'email':        user.email,
        'address':      user.address,
        'phone_number': user.phone_number,
        'role_name':    role_name,
        'team_name':    team_name,
        'account_id':   account_id,
        'password_mask': '••••••••',

    }

    # 5) Render the profile template
    return render(request, 'health_check/profile.html', context)

    
#Rest password page view
def reset_password(request):
    if (request.method == 'POST'):
        new_password = request.POST.get('new_password')   
        r_new_password = request.POST.get('r_new_password')

        if new_password==r_new_password:
            user=request.user 
            user.set_password(new_password) #securely updates the password
            user.save()
            messages.success(request, "Password has been reset successfully")
            return redirect('login') #redirects to login page
        else:
            messages.error(request, "Password do not match. Please try again")
    return render(request, 'health_check/resetpassword.html' )