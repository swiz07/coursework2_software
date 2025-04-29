from django.contrib import admin
from .models import Team, Card, Vote, User, Session, Department

admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Card)
admin.site.register(Vote)
admin.site.register(User)
admin.site.register(Session)
