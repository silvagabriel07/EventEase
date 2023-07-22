from django import forms
from .models import phone_number_validators
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm, ResetPasswordForm
from .models import User

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control custom-form-width', 'placeholder': 'Senha',})
        self.fields['password1'].label = 'Senha:'
        self.fields['password2'].widget.attrs.update({'class': 'form-control custom-form-width', 'placeholder': 'Senha (novamente)',})
        self.fields['password2'].label = 'Confirmar Senha:'
        self.fields['username'].widget.attrs.update({'class': 'form-control custom-form-width', 'placeholder': 'Nome de usuário'})
        self.fields['username'].label = 'Nome de Usuário:'
        self.fields['email'].widget.attrs.update({'class': 'form-control custom-form-width', "placeholder": "Endereço de email"})
        self.fields['email'].label = 'Endereço de email:'

    
    idade = forms.IntegerField(required=True, label='Idade:', widget=forms.NumberInput(attrs={'class': 'form-control custom-form-width', 'placeholder': 'Idade'}))
    # Não obrigatórios
    phone_number = forms.CharField(required=False, label='Número de telefone:', max_length=14, validators=[phone_number_validators], widget=forms.TextInput(attrs={'id': 'id_phone_number', 'class': 'form-control custom-form-width', 'placeholder': '+00 00000-0000'}))
    
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

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control custom-form-width', "placeholder": "Endereço de email"})
        self.fields['login'].label = 'Endereço de email:'
        self.fields['password'].widget.attrs.update({'class': 'form-control custom-form-width', 'placeholder': 'Senha',})
        self.fields['password'].label = 'Senha:'

class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs.update({'class': 'form-control custom-form-width', 'placeholder': 'Senha atual',})
        self.fields['password1'].widget.attrs.update({'class': 'form-control custom-form-width', 'placeholder': 'Senha nova',})
        self.fields['password2'].widget.attrs.update({'class': 'form-control custom-form-width', 'placeholder': 'Senha nova (novamente)',})

class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control custom-form-width'})