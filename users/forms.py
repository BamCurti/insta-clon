from django import forms
from django.contrib.auth.models import User
from users.models import Profile

class ProfileForm(forms.Form):
    website = forms.URLField(max_length=200, required=True)
    biography = forms.CharField(max_length=500, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    picture = forms.ImageField(required=True)

class SignUpForm(forms.Form):
    username = forms.CharField(label=False, min_length=4, max_length=50, required=True, 
    widget=forms.TextInput(
        attrs={
            'placeholder':'username',
            'class':'form-control',
            'required':'True'
        }
    ))
    password = forms.CharField(max_length=70, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput())

    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    email = forms.CharField(max_length=70, widget=forms.EmailInput())

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username="username").exists()

        if username_taken:
            raise forms.ValidationError('Username is already taken')
        
        return username

    def clean(self):
        """Verify if passwords match"""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords does not match')

        return data

    def clean_email(self):
        """Verify if email is already taken"""
        email = self.cleaned_data['email']
        email_taken = User.objects.filter(email=email).exists
        
        if email_taken:
            raise forms.ValidationError('The email {} is already taken'.format(email))

        return email

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create(**data)
        profile = Profile(user)
        profile.save()