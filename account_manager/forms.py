from django import forms
from allauth.account.forms import SignupForm
from .models import User

class CustomSignupForm(SignupForm):
    idade = forms.IntegerField(required=True)
    field_order = ['username', 'email', 'idade', 'password1','password2']

    def clean_idade(self):
        idade = self.cleaned_data["idade"]
        if not idade:
            raise forms.ValidationError("A idade é obrigatória.")
        return idade

    def save(self, request):
        user = User.objects.create_user(
        email=self.cleaned_data['email'],
        username=self.cleaned_data['username'],
        password=self.cleaned_data['password1'],
        idade=self.cleaned_data['idade']
        # adicione outros campos extras aqui
        )
        return user
