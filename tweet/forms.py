from django import forms
from .models import Tweet,Comment,Profile, review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = review
        fields = ['rating', 'comment']


class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model =User
        fields = ('username', 'email', 'password1', 'password2')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'bio', 'images']