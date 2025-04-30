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
    
    sid = request.GET.get("session")
    if sid:
        request.session["current_session_id"] = sid
        return get_object_or_404(Session, session_id=sid)
    stored = request.session.get("current_session_id")
    if stored:
        s = Session.objects.filter(session_id=stored).first()
        if s:
            return s
    return Session.objects.filter(session_status="active")\
                          .order_by("-session_started")\
                          .first()

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
    # ─────── Determine current session ───────
    session_obj = current_session(request)
    if not session_obj:
        return redirect('choose_session')

    # ─────── Build department ───────
    role = request.user.role
    if role == "team_leader" and request.user.team:
        departments = [request.user.team.department.department_name]
        teams_qs    = Team.objects.filter(team_id=request.user.team.team_id)
    elif role == "dept_leader" and request.user.team:
        dept        = request.user.team.department
        departments = [dept.department_name]
        teams_qs    = Team.objects.filter(department_id=dept)
    else:
        departments = list(
            Department.objects
                      .order_by("department_name")
                      .values_list("department_name", flat=True)
        )
        teams_qs = Team.objects.select_related("department_id") \
                               .order_by("department_id__department_name", "team_name")

    # ─────── Filter by chosen department ───────
    selected_department = request.GET.get("department", "all")
    if selected_department != "all" and len(departments) > 1:
        teams_qs = teams_qs.filter(department_id__department_name=selected_department)

    # ─────── Sidebar team list + default selection ───────
    team_list = [(t.team_id, t.team_name) for t in teams_qs]
    selected_team = request.GET.get("team")
    if not selected_team and team_list:
        selected_team = str(team_list[0][0])

    # ─────── Aggregate votes per team in this session ───────
    # pre-filter to just this session
    base_qs = Vote.objects.filter(session_id=session_obj)
    team_data = {}

    for t in teams_qs:
        red = amber = green = 0
        for row in base_qs.filter(user_id__team=t) \
                  .values("vote_value") \
                  .annotate(ct=Count("vote_value")):
            v, ct = str(row["vote_value"]), row["ct"]

            if v in {"1", "red"}:
                red   += ct                #  ← ADD instead of =
            elif v in {"2", "amber", "yellow"}:
                amber += ct
            elif v in {"3", "green"}:
                green += ct

        team_data[t.team_id] = {
            "name":  t.team_name,
            "red":   red,
            "amber": amber,
            "green": green,
}

    # ─────── Manager flag ───────
    is_manager = (
        role in {"dept_leader", "senior_manager"} or
        request.user.is_staff or
        request.user.is_superuser
    )

    return render(request, "health_check/statistics.html", {
        "sessions":            Session.objects.order_by("-session_started"),
        "current_session":     session_obj,
        "departments":         departments,
        "selected_department": selected_department,
        "team_list":           team_list,
        "selected_team":       selected_team,
        "team_data_json":      json.dumps(team_data),
        "is_manager":          is_manager,
        "colors":              ["red", "amber", "green"],
    })

    

def recalc_card_aggregates(card):
   
    qs = Vote.objects.filter(card_id=card, session_id=card.session_id)
    counts = qs.values("vote_value")\
               .annotate(ct=Count("vote_value"))\
               .values_list("vote_value", "ct")
    
    card.card_red_vote    = 0
    card.card_yellow_vote = 0
    card.card_green_vote  = 0

    for value, ct in counts:
        if value == "red":
            card.card_red_vote = ct
        elif value == "amber":
            card.card_yellow_vote = ct
        elif value == "green":
            card.card_green_vote = ct

    
    if card.card_green_vote >= card.card_yellow_vote \
       and card.card_green_vote >= card.card_red_vote:
        card.colour_code = "green"
    elif card.card_yellow_vote >= card.card_red_vote:
        card.colour_code = "amber"
    else:
        card.colour_code = "red"

    card.save()

@login_required
def voting_page(request):
    session = current_session(request)
    if not session:
        return redirect("choose_session")

    request.session["current_session_id"]      = session.session_id
    request.session["current_session_display"] = session.session_name

    if request.method == "POST":
        card_id  = request.POST.get("card_id")
        progress = request.POST.get("vote_opinion")  
        if not (card_id and progress):
            messages.error(request, "Please select a Progress value.")
            return redirect("voting_page")

        card = get_object_or_404(Card, card_id=card_id, session_id=session)

        
        colour_map = {
            "Unsatisfied":          "red",
            "Partially Satisfied": "yellow",
            "Satisfied":            "green",
        }
        vote_value = colour_map[progress]

        Vote.objects.update_or_create(
            user_id    = request.user,
            card_id    = card,
            session_id = session,
            defaults   = {
                "vote_value":   vote_value,
                "vote_opinion": progress
            }
        )

       
        recalc_card_aggregates(card)

        messages.success(request, f"Your vote for “{card.card_name}” has been saved.")
        return redirect("voting_page")

    # GET
    user_cards   = Card.objects.filter(session_id=session)
    user_history = (
        Vote.objects
            .filter(session_id=session)
            .select_related("card_id", "user_id")
            .order_by("-created_at")
    )

    return render(request, "health_check/VotingPage.html", {
        "user_cards":   user_cards,
        "user_history": user_history,
    })


def recalc_card_aggregates(card):
   
    qs = Vote.objects.filter(card_id=card, session_id=card.session_id)
    counts = qs.values("vote_value") \
               .annotate(ct=Count("vote_value"))

    card.card_red_vote    = 0
    card.card_yellow_vote = 0
    card.card_green_vote  = 0

    for entry in counts:
        val, ct = entry["vote_value"], entry["ct"]
        if val == "red":
            card.card_red_vote = ct
        
        elif val in ("yellow", "amber"):
            card.card_yellow_vote = ct
        elif val == "green":
            card.card_green_vote = ct

   
    if card.card_green_vote >= card.card_yellow_vote \
       and card.card_green_vote >= card.card_red_vote:
        card.colour_code = "green"
    elif card.card_yellow_vote >= card.card_red_vote:
        card.colour_code = "amber"
    else:
        card.colour_code = "red"

    card.save()

@login_required
def all_history(request):
    sess_id = request.session.get("current_session_id")
    if not sess_id:
        return redirect("choose_session")

    current_session = get_object_or_404(Session, session_id=sess_id)

    # allow sorting & filtering 
    sort_key = request.GET.get("sort", "time")
    query    = request.GET.get("q", "")

    # map sort keys → model fields
    FIELD_MAP = {
        "time": "created_at",
        "card": "card_id__card_name",
        "vote": "vote_value",
    }
    sort_field = FIELD_MAP.get(sort_key, "created_at")

    qs = Vote.objects.filter(session_id=current_session)
    if query:
        qs = qs.filter(
            Q(card_id__card_name__icontains=query) |
            Q(vote_opinion__icontains=query)
        )

    user_votes = qs.select_related("card_id")\
                   .order_by(f"-{sort_field}")

    return render(request, "health_check/all_history.html", {
        "user_votes":     user_votes,
        "current_sort":   sort_key,
        "query":          query,
        "sort_options":   SORT_OPTS,
        "current_session": current_session,
    })


@login_required
def choose_session(request):
    sessions       = Session.objects.order_by("-session_started")
    current_id     = request.session.get("current_session_id")
    current_sess   = None
    if current_id:
        current_sess = get_object_or_404(Session, session_id=current_id)
    return render(request, "health_check/choose_session.html", {
        "sessions":        sessions,
        "current_session": current_sess,
    })

def set_session(request, session_id):
    request.session['current_session_id'] = session_id
    return redirect('voting_page')