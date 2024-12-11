from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm  # Add this import


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create profile with user_type
            Profile.objects.create(
                user=user,
                user_type=self.cleaned_data.get('user_type', 'MENTEE')
            )
        return user
    

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'displayname', 'info']
        labels = {
            'image': 'Profile Picture',
            'displayname': 'Display Name',
            'info': 'About Me'
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'displayname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your display name'
            }),
            'info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about yourself'
            })
        }
        
        
class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

from allauth.account.forms import SignupForm

from django import forms
from allauth.account.forms import SignupForm
from .models import Profile

class CustomSignupForm(SignupForm):
    user_type = forms.ChoiceField(
        choices=Profile.USER_TYPES,
        widget=forms.RadioSelect,
        label='I want to be a'
    )

    def save(self, request):
        user = super().save(request)
        user_type = self.cleaned_data.get('user_type')
        Profile.objects.create(user=user, user_type=user_type)
        return user
    
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

class MentorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create profile after user is saved
            Profile.objects.get_or_create(
                user=user,
                defaults={'user_type': 'MENTOR'}
            )
        return user

class MenteeRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create profile after user is saved
            Profile.objects.get_or_create(
                user=user,
                defaults={'user_type': 'MENTEE'}
            )
        return user

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email Address')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from .models import Profile

# Your existing forms (ProfileForm and EmailForm) remain unchanged...

class MentorSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        Profile.objects.create(
            user=user,
            user_type='MENTOR'
        )
        return user

class MenteeSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        Profile.objects.create(
            user=user,
            user_type='MENTEE'
        )
        return user
    

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'displayname', 'info']
        labels = {
            'image': 'Profile Picture',
            'displayname': 'Display Name',
            'info': 'About Me'
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'displayname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your display name'
            }),
            'info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about yourself'
            })
        }