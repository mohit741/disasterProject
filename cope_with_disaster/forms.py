from django import forms
from .models import Subscriber, Rescuer


class EmailSubForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone', 'maxlength':10}))
    lat = forms.DecimalField(widget=forms.TextInput(attrs={'id' : 'lat', 'class': 'form-control', 'placeholder': 'Latitude', 'maxlength':10}))
    lon = forms.DecimalField(widget=forms.TextInput(attrs={'id' : 'lon', 'class': 'form-control', 'placeholder': 'Longitude', 'maxlength':10}))

    class Meta:
        model = Subscriber
        fields = ('email','phone','lon','lat')
