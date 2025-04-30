from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Subquery, OuterRef, Q, Count
from django.http import HttpResponse, HttpResponseForbidden
from health_check.models import Department, Team, User, Vote, Card, Session 
import json
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

def current_session(request):
    # 1) override via GET
    sid = request.GET.get("session")
    if sid:
        request.session["current_session_id"] = sid
        return get_object_or_404(Session, id=sid)
    # 2) falling back to stored
    stored = request.session.get("current_session_id")
    if stored:
        s = Session.objects.filter(id=stored).first()
        if s:
            return s
    # 3) last active
    return Session.objects.filter(status="active").order_by("-date").first()

SORT_OPTS = [("time", "Time"),
             ("card", "Card"),
             ("vote", "Vote")]

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



@login_required
def statistics(request):
    # ──────────────────────── session ────────────────────────────────────────
    session_obj = current_session(request)

    # ───────────────────── role + scope ─────────────────────────────────────
    role = request.user.role
    if role == "team_leader" and request.user.team:
        departments = [request.user.team.department.name]
        teams_qs    = Team.objects.filter(id=request.user.team.id)
    elif role == "dept_leader" and request.user.team:
        dept = request.user.team.department
        departments = [dept.name]
        teams_qs    = Team.objects.filter(department=dept)
    else:
        departments = list(Department.objects.order_by("name")
                                              .values_list("name", flat=True))
        teams_qs    = Team.objects.select_related("department") \
                                  .order_by("department__name", "name")

    # ─────────────── filter by department GET ────────────────────────────────
    selected_department = request.GET.get("department", "all")
    if selected_department != "all" and len(departments) > 1:
        teams_qs = teams_qs.filter(department__name=selected_department)

    # ──────────────── build sidebar list & default team ───────────────────────
    team_list = [(t.id, t.name) for t in teams_qs]
    selected_team = request.GET.get("team")
    if not selected_team and team_list:
        selected_team = str(team_list[0][0])

    # ─────────────────── aggregate ALL votes in this session ─────────────────
    team_data = {}
    for t in teams_qs:
        votes = Vote.objects.filter(user__team=t, session=session_obj)
        team_data[t.id] = {
            "name":  t.name,
            "red":   votes.filter(vote_choice="red").count(),
            "amber": votes.filter(vote_choice="yellow").count(),
            "green": votes.filter(vote_choice="green").count(),
        }

    # ────────────────────── manager flag ─────────────────────────────────────
    is_manager = (
        role in {"dept_leader", "senior_manager"}
        or request.user.is_staff
        or request.user.is_superuser
    )

    return render(request, "health_check/statistics.html", {
        "sessions":            list(Session.objects.order_by("-date")),
        "current_session":     session_obj,
        "departments":         departments,
        "selected_department": selected_department,
        "team_list":           team_list,
        "selected_team":       selected_team,
        "team_data_json":      json.dumps(team_data),
        "is_manager":          is_manager,
        "colors":              ["red", "amber", "green"],
    })


@login_required
def voting_page(request):
   
    # 1) Determine current session
    session_id = (request.GET.get('session')
                  or request.session.get('current_session_id'))
    if not session_id:
        return redirect('choose_session')

    session = get_object_or_404(Session, id=session_id)
    request.session['current_session_id']      = session.id
    request.session['current_session_display'] = session.date.strftime("%-d %b %Y %H:%M")

    # 2) Handle new vote submission
    if request.method == 'POST':
        card_id     = request.POST.get('card_id')
        vote_choice = request.POST.get('vote_choice')
        reason      = request.POST.get('reason', '')
        if card_id and vote_choice:
            card = get_object_or_404(Card, id=card_id)
            Vote.objects.create(
                session     = session,
                user        = request.user,
                card        = card,
                vote_choice = vote_choice,
                reason      = reason
            )
        return redirect('voting_page')

    # 3) Build aggregated counts for each card
    user_cards = []
    for c in Card.objects.all():
        latest_ids = (
            Vote.objects
                .filter(card=c, session=session)
                .values('user')
                .annotate(latest=Max('id'))
                .values_list('latest', flat=True)
        )
        vs = Vote.objects.filter(id__in=latest_ids)
        c.red_count    = vs.filter(vote_choice='red').count()
        c.yellow_count = vs.filter(vote_choice='yellow').count()
        c.green_count  = vs.filter(vote_choice='green').count()
        user_cards.append(c)

    # 4) Build vote history

    user_history = Vote.objects.filter(session=session) \
                           .select_related('card','user') \
                           .order_by('-created_at')

    return render(request, 'health_check/VotingPage.html', {
        'user_cards':   user_cards,
        'user_history': user_history,
    })

@login_required
def all_history(request):
    # 1) enforce session
    sess_id = request.session.get('current_session_id')
    if not sess_id:
        return redirect(f"{reverse('choose_session')}?next=all_history")

    current_session = get_object_or_404(Session, id=sess_id)

    # 2) get sort & filter params
    sort_key = request.GET.get("sort", "time")
    query    = request.GET.get("q", "")

    # 3) map frontend keys → model fields
    valid_sort_fields = {
        "time": "created_at",
        "card": "card__title",
        "vote": "vote_choice",
    }
    sort_field = valid_sort_fields.get(sort_key, "created_at")

    # 4) base queryset _for this session_
    qs = Vote.objects.filter(session=current_session)

    # 5) search filter
    if query:
        qs = qs.filter(
            Q(card__title__icontains=query) |
            Q(reason__icontains=query)
        )

    # 6) annotate & order
    user_votes = (
        qs
        .select_related("card")
        .order_by(f"-{sort_field}")
    )

    context = {
        "user_votes":     user_votes,
        "current_sort":   sort_key,
        "query":          query,
        "sort_options":   SORT_OPTS,
        "current_session": current_session,
    }
    return render(request, "health_check/all_history.html", context)


def choose_session(request):
    sessions = Session.objects.order_by('-date')
    current_id = request.session.get('current_session_id')
    current_session = None
    if current_id:
        current_session = get_object_or_404(Session, id=current_id)
    return render(request, 'health_check/choose_session.html', {
        'sessions': sessions,
        'current_session': current_session,
    })

def set_session(request, session_id):
    request.session['current_session_id'] = session_id
    return redirect('voting_page')