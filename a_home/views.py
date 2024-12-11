from django.shortcuts import render
from a_users.models import Profile

def home_view(request):
    # Get all profiles where user_type is 'MENTOR'
    mentors = Profile.objects.filter(user_type='MENTOR')
    return render(request, 'home.html', {'mentors': mentors})