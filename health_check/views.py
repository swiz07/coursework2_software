from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Card, Vote
from django.shortcuts import get_object_or_404
from django.db.models import Max, Subquery, OuterRef

# Register view
# views.py
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}!')
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'health_check/register.html', {'form': form})

# Home page view
def home(request):
    return render(request, 'home.html')
 
def enghome(request):
    return render(request, 'enghome.html')


def deptLeaderHome(request):
    return render(request, 'DeptLeaderHome.html') 



#def SenManagerHome(request):
 #   return render(request, 'SenManagerHome.html')


def engineer_statistics(request):
    return render(request, 'EngineerStatistics.html')

def engineer_statistics_viewall(request):
    
    cards = [
        {"id": 1, "title": "System Stability", "red": 25, "yellow": 15, "green": 10},
        {"id": 2, "title": "Delivery Speed", "red": 12, "yellow": 20, "green": 30},
        # ...
    ]
    return render(request, 'EngineerStatisticsViewAll.html', {"cards": cards})

def engineer_statistics_card_detail(request, card_id):
    
    card = {
        "id": card_id,
        "title": "System Stability",
        "red": 25,
        "yellow": 15,
        "green": 10,
        "description": "Detailed breakdown for card ID " + str(card_id),
    }
    return render(request, 'EngineerStatisticsCardDetail.html', {"card": card})



@login_required
def voting_page(request):
    user = request.user
    user_cards = Card.objects.all()  

    # Compute vote counts per card
    for c in user_cards:
        latest_votes = Vote.objects.filter(card=c).values('user').annotate(latest_id=Max('id'))
        vote_ids = [entry['latest_id'] for entry in latest_votes]
        latest_votes_qs = Vote.objects.filter(id__in=vote_ids)

        c.red_count = latest_votes_qs.filter(card=c, vote_choice='red').count()
        c.yellow_count = latest_votes_qs.filter(card=c, vote_choice='yellow').count()
        c.green_count = latest_votes_qs.filter(card=c, vote_choice='green').count()


    user_history = Vote.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        vote_choice = request.POST.get('vote_choice')
        reason = request.POST.get('reason', '')

        card = get_object_or_404(Card, id=card_id)

        # Save as new vote history entry
        Vote.objects.create(
            user=user,
            card=card,
            vote_choice=vote_choice,
            reason=reason
        )

        return redirect('voting_page')

    return render(request, 'VotingPage.html', {
        'user_cards': user_cards,
        'user_history': user_history,
    })



@login_required
def voting_history(request):

    """ Displays the user's own voting history """
    user_votes = Vote.objects.filter(user=request.user).select_related('card').order_by('-created_at')
    return render(request, 'VotingHistoryPage.html', {
        'user_votes': user_votes
    })
