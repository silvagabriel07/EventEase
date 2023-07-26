from django import forms
from account_manager.models import User, PhoneNumber


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'idade', 'user_img']

