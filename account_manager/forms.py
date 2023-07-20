from django import forms
from .models import phone_number_validators
from allauth.account.forms import SignupForm
from .models import User

class CustomSignupForm(SignupForm):
    idade = forms.IntegerField(required=True)
    # Não obrigatórios
    phone_number = forms.CharField(required=False, max_length=14, validators=[phone_number_validators], widget=forms.TextInput(attrs={'placeholder': '+00 00000-0000'}))
  
    field_order = ['username', 'email', 'idade', 'password1', 'password2', 'user_img']

    def clean_idade(self):
        idade = self.cleaned_data["idade"]
        if idade:
            if idade < 14:
                self.add_error('idade', 'Menores de 14 anos não podem se cadastrar.')
            else:
                return idade
        else:
            self.add_error('idade', 'A idade deve ser informada.')

    def save(self, request):
        user = User.objects.create_user(
        email=self.cleaned_data['email'],
        username=self.cleaned_data['username'],
        password=self.cleaned_data['password1'],
        idade=self.cleaned_data['idade'],
        )
        user.phonenumber_set.create(phone_number=self.cleaned_data['phone_number'])
        return user
