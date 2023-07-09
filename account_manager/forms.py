from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': '+00 00000-0000'})),
    idade = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    field_order = ['username', 'email', 'idade', 'phone_number', 'password1', 'password2']
