from django import forms
from social.models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Username", widget=forms.TextInput({ 'placeholder': "Enter Username", 'class':'form-control' }))
    email = forms.CharField(help_text="Email", widget=forms.TextInput({ 'placeholder': "Enter Email", 'class':'form-control' }))
    first_name = forms.CharField(help_text="First Name", widget=forms.TextInput({ 'placeholder': "Enter First Name", 'class':'form-control' }))
    last_name = forms.CharField(help_text="Last Name", widget=forms.TextInput({ 'placeholder': "Enter Last Name", 'class':'form-control' }))
    password = forms.CharField(help_text="Password", widget=forms.PasswordInput({ 'placeholder': "Enter Password", 'class':'form-control' }))

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password')

class AuthorForm(forms.ModelForm):
    image = forms.ImageField(help_text="Profile Picture", required=False)

    class Meta:
        model = Author
        fields = ('image', )

class ImageUploadForm(forms.Form):
    image = forms.ImageField()