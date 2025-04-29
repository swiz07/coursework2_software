from django.shortcuts import render, redirect
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse     
from .models import Vote, Card, Session, User 
from django.utils import timezone

def register(request):
        if request.method == 'POST':
            email = request.POST['email']
            fullname = request.POST['name']
            password = request.POST['password']
            address = request.POST['address']
            phone_number = request.POST['phone']
            role_name = request.POST['role']
            department_id = request.POST.get('department')
            team_id = request.POST.get('team')
            
            role=Role.objects.get(name=role_name)
            department = None
            if department_id:
                department = Department.objects.get(department_id=department_id)
        
            team = None
            if team_id:
                team = Team.objects.get(team_id=team_id)
            # Create the user with the role
            user = User.objects.create_user(
                username = email,
                email=email, 
                fullname=fullname,
                password=password,
                address=address,
                phone_number=phone_number,
                role=role,
                department=department,
                team=team,
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

        departments = Department.objects.all()
        teams = Team.objects.all()
        return render(request, 'health_check/register.html', {'departments': departments, 'teams': teams})

class CustomLoginView(LoginView):

    template_name = 'health_check/login.html' 

    def get_success_url(self):
        user = self.request.user
        print(f"User: {user.email}, Role: {user.role}")
        role = getattr(user, 'role', None)
        if role:
             print(f"Role flags - Engineer: {role.is_engineer}, Team Leader: {role.is_team_leader}, Department Leader: {role.is_department_leader}, Senior Manager: {role.is_senior_manager}")  # Debug line
        if role.is_engineer:
            return reverse('enghome')
        elif role.is_team_leader:
            return reverse('teamLeaderHome')
        elif role.is_department_leader:
            return reverse('deptLeaderHome')
        elif role.is_senior_manager:
            return reverse('SenManagerHome')
        else:
            return reverse('home')


 # Log out
def logout_view(request):
    logout(request)
    return redirect('home') 


    # Home page view
def home(request):
        return render(request, 'home.html')

    #Engineer page view
def enghome(request):
    is_engineer = False
    is_team_leader = False
    is_department_leader = False
    is_senior_manager = False

    #get their role
    if request.user.is_authenticated  and hasattr(request.user, 'role'):
        role = request.user.role
        is_engineer = role.is_engineer
        is_team_leader = role.is_team_leader
        is_department_leader = role.is_department_leader
        is_senior_manager = role.is_senior_manager

    #displays cardds
    if request.user.is_authenticated and request.user.team:
        cards = Card.objects.filter(session_id__team_id=request.user.team)
    else:
        cards = []  
 
    return render(request, 'enghome.html', {
        'is_engineer': is_engineer,
        'is_team_leader': is_team_leader,
        'is_department_leader': is_department_leader,
        'is_senior_manager': is_senior_manager,
        'cards': cards, 
    })

def teamLeader(request):
    is_engineer = False
    is_team_leader = False
    is_department_leader = False
    is_senior_manager = False

    if request.user.is_authenticated and hasattr(request.user, 'role'):
        role = request.user.role
        is_engineer = role.is_engineer
        is_team_leader = role.is_team_leader
        is_department_leader = role.is_department_leader
        is_senior_manager = role.is_senior_manager

    #displays cardds
    if request.user.is_authenticated and request.user.team:
        cards = Card.objects.filter(session_id__team_id=request.user.team)
    else:
        cards = []  
    return render(request, 'teamLeaderHome.html', {
        'is_engineer': is_engineer,
        'is_team_leader': is_team_leader,
        'is_department_leader': is_department_leader,
        'is_senior_manager': is_senior_manager,
        'cards': cards
    }) 

def deptLeaderHome(request):
    is_engineer = False
    is_team_leader = False
    is_department_leader = False
    is_senior_manager = False

    if request.user.is_authenticated and hasattr(request.user, 'role'):
        role = request.user.role
        is_engineer = role.is_engineer
        is_team_leader = role.is_team_leader
        is_department_leader = role.is_department_leader
        is_senior_manager = role.is_senior_manager

        #displays teams
    if request.user.department:
        teams = Team.objects.filter(department_id=request.user.department)
    else:
        teams = [] 

    return render(request, 'DeptLeaderHome.html', {
        'is_engineer': is_engineer,
        'is_team_leader': is_team_leader,
        'is_department_leader': is_department_leader,
        'is_senior_manager': is_senior_manager,
        'teams': teams
    })  


def SenManagerHome(request):
    is_engineer = False
    is_team_leader = False
    is_department_leader = False
    is_senior_manager = False

    if request.user.is_authenticated and hasattr(request.user, 'role'):
        role = request.user.role
        is_engineer = role.is_engineer
        is_team_leader = role.is_team_leader
        is_department_leader = role.is_department_leader
        is_senior_manager = role.is_senior_manager

#displays Departments
    if request.user.is_authenticated:
        departments = Department.objects.all()
    else:
        departments = [] 

    return render(request, 'SenManagerHome.html', {
        'is_engineer': is_engineer,
        'is_team_leader': is_team_leader,
        'is_department_leader': is_department_leader,
        'is_senior_manager': is_senior_manager,
        'departments': departments 
    }) 

    
def profile(request):
        # 1) Redirect any anonymous user to your login
        if not request.user.is_authenticated:
            return redirect('login')

        # 2) Safe to grab `request.user` fields now
        user = request.user

        # 3) Pull related names, guarding against None
        role_name  = user.role.name                       if user.role else ''
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
            'is_engineer': user.role.is_engineer if user.role else False,
            'is_team_leader': user.role.is_team_leader if user.role else False,
            'is_department_leader': user.role.is_department_leader if user.role else False,
            'is_senior_manager': user.role.is_senior_manager if user.role else False,

        }

        # 5) Render the profile template
        return render(request, 'health_check/profile.html', context)

@login_required
def voting_page(request):
    is_engineer = False
    is_team_leader = False
    is_department_leader = False
    is_senior_manager = False

    if request.user.is_authenticated and hasattr(request.user, 'role'):
        role = request.user.role
        is_engineer = role.is_engineer
        is_team_leader = role.is_team_leader
        is_department_leader = role.is_department_leader
        is_senior_manager = role.is_senior_manager

    if request.user.is_authenticated and request.user.team:
        cards = Card.objects.filter(session_id__team_id=request.user.team)

        #get the total number of cards
        total_cards = cards.count()


#to get how many cards they have voted
        voted_card_ids = Vote.objects.filter(user_id=request.user, card_id__in=cards).values_list('card_id', flat=True)
        voted_cards = cards.filter(card_id__in=voted_card_ids)
        not_voted_cards = cards.exclude(card_id__in=voted_card_ids)

        

        voted_count = voted_cards.count()
        not_voted_count = not_voted_cards.count()

        percentage_voted = round((voted_count / total_cards) * 100) if total_cards > 0 else 0
    else:
        cards = Card.objects.none()
        voted_cards = not_voted_cards = []
        voted_count = not_voted_count = percentage_voted = 0
        total_cards = 0

    return render(request, 'health_check/voting_page.html', {
        'is_engineer': is_engineer,
        'is_team_leader': is_team_leader,
        'is_department_leader': is_department_leader,
        'is_senior_manager': is_senior_manager,
        'page_title': 'Voting Page',
        'cards': cards,
        'voted_count': voted_count,
        'not_voted_count': not_voted_count,
        'voted_cards': voted_cards,
        'not_voted_cards': not_voted_cards,
        'percentage_voted': percentage_voted,
        'total_cards': total_cards,
    })


        
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

def load_teams(request):
    department_id = request.GET.get('department_id')
    teams = Team.objects.filter(department_id=department_id).order_by('team_name')
    return render(request, 'teams/team_dropdown_list_options.html', {'teams': teams})   

#submits the votes
@login_required
def submit_votes(request):
    if request.method == 'POST':
        user = request.user
        card_id = request.POST.get('card_id')
        session_id = request.POST.get('session_id')

        opinion = request.POST.get(f'opinion-{card_id}')
        progress = request.POST.get(f'progress-{card_id}')

        if not opinion or not progress:
            messages.error(request, "Both opinion and progress must be selected.")
            return redirect('voting_page')

        card = Card.objects.get(pk=card_id)
        session = Session.objects.get(pk=session_id)

        Vote.objects.update_or_create(
            user_id=user,
            card_id=card,
            session_id=session,
            defaults={
                'vote_value': opinion,
                'vote_opinion': progress,
            }
        )

        #  Update card colour 
        update_card_colour(card.card_id)
        messages.success(request, f"Vote for '{card.card_name}' saved successfully.")
        return redirect('voting_page')  

#to get card color and number of red, green, yellow votes
def update_card_colour(card_id):
    votes = Vote.objects.filter(card_id=card_id)
    vote_counts = {"red": 0, "yellow": 0, "green": 0}

    for vote in votes:
        if vote.vote_value == 'negative':
            vote_counts["red"] += 1
        elif vote.vote_value == 'neutral':
            vote_counts["yellow"] += 1
        elif vote.vote_value == 'positive':
            vote_counts["green"] += 1

    max_vote = max(vote_counts, key=vote_counts.get)
    
    card = Card.objects.get(pk=card_id)
    card.colour_code = max_vote
    card.card_red_vote = vote_counts["red"]
    card.card_yellow_vote = vote_counts["yellow"]
    card.card_green_vote = vote_counts["green"]
    card.save()


def get_vote_percentages(card_id):
    votes = Vote.objects.filter(card_id=card_id)
    vote_counts = {"red": 0, "yellow": 0, "green": 0}
    total_votes = votes.count()

    if total_votes == 0:
        return {"red": 0, "yellow": 0, "green": 0}

    for vote in votes:
        if vote.vote_value == 'negative':
            vote_counts["red"] += 1
        elif vote.vote_value == 'neutral':
            vote_counts["yellow"] += 1
        elif vote.vote_value == 'positive':
            vote_counts["green"] += 1

    vote_percentages = {
        "red": round((vote_counts["red"] / total_votes) * 100, 2),
        "yellow": round((vote_counts["yellow"] / total_votes) * 100, 2),
        "green": round((vote_counts["green"] / total_votes) * 100, 2),
    }

    return vote_percentages