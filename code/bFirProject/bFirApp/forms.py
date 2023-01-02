from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'User Name'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
    adhaarId = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'adhaar'}), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'phone'}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'address'}), required=True)

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2', 'adhaarId', 'phone', 'address']