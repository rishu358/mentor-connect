from django.urls import path
from a_users.views import *

urlpatterns = [
    path('', profile_view, name="profile"),  # Keep this for the user's own profile
    path('<str:username>/', profile_view, name="profile"),  # Add this new pattern for viewing other users' profiles
    path('edit/', profile_edit_view, name="profile-edit"),
    path('onboarding/', profile_edit_view, name="profile-onboarding"),
    path('settings/', profile_settings_view, name="profile-settings"),
    path('emailchange/', profile_emailchange, name="profile-emailchange"),
    path('emailverify/', profile_emailverify, name="profile-emailverify"),
    path('delete/', profile_delete_view, name="profile-delete"),
]