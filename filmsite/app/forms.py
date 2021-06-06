from django import forms
from django.db.models import fields
from app.models import *
from django.contrib.auth.forms import UserCreationForm

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"

class OpinionForm(forms.ModelForm):
    rate = forms.ChoiceField(choices=Opinion.RATES, widget=forms.RadioSelect(attrs={'class': 'inline d-flex justify-content-around no-bullets text-center p-0'}))

    class Meta:
        model = Opinion
        fields = ['rate', 'is_favourite', 'want_to_watch', 'contents']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'contents']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email",)

class UserUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = UserProfile
        fields = ['avatar', 'user']

