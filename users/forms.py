from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):

    SPOTIFY_CHOICES=[
        ('yes','Yes'),
        ('no','No')
    ]

    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    spotify = forms.CharField(label="Do you have a spotify account?", widget=forms.Select(choices=SPOTIFY_CHOICES))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'spotify']
