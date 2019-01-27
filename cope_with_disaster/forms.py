from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Subscriber, Rescuer, User


class EmailSubForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone', 'maxlength':10}))
    lat = forms.DecimalField(widget=forms.TextInput(attrs={'id' : 'lat', 'class': 'form-control', 'placeholder': 'Latitude', 'maxlength':10}))
    lon = forms.DecimalField(widget=forms.TextInput(attrs={'id' : 'lon', 'class': 'form-control', 'placeholder': 'Longitude', 'maxlength':10}))

    class Meta:
        model = Subscriber
        fields = ('email','phone','lon','lat')


class UserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class RegForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'maxlength':100}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone', 'maxlength':10}))
    lat = forms.DecimalField(widget=forms.TextInput(attrs={'id' : 'lat', 'class': 'form-control', 'placeholder': 'Latitude', 'maxlength':10}))
    lon = forms.DecimalField(widget=forms.TextInput(attrs={'id' : 'lon', 'class': 'form-control', 'placeholder': 'Longitude', 'maxlength':10}))

    class Meta:
        model = Rescuer
        fields = ('name','phone','lon','lat')

    def save(self, commit=True):
        profile = super(RegForm, self).save(commit=False)
        profile.name = self.cleaned_data["name"]
        profile.lat = self.cleaned_data["lat"]
        profile.lon = self.cleaned_data["lon"]
        profile.phone = self.cleaned_data["phone"]
        if commit:
            profile.save()
        return profile
