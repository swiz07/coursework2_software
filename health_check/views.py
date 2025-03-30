from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User, Role  # Ensure you import your User and Role models

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        fullname = request.POST['name']
        password = request.POST['password']
        address = request.POST['address']
        phone_number = request.POST['phone']
        role_name = request.POST['role']

        try:
            # Attempt to get the Role object
            role = Role.objects.get(role_name=role_name)
        except Role.DoesNotExist:
            messages.error(request, 'Selected role does not exist.')
            return render(request, 'health_check/register.html')

        # Create the user with the role
        user = User.objects.create_user(
            email=email,
            fullname=fullname,
            password=password,
            address=address,
            phone_number=phone_number,
            role=role  # Pass the role here
        )

        # Log the user in after registration
        login(request, user)

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

# Home page view
def home(request):
    return render(request, 'home.html')
 
def enghome(request):
    return render(request, 'enghome.html')