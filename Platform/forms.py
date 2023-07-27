from django import forms
from account_manager.models import User, PhoneNumber


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control custom-form-width', 'placeholder': '+00 00000-0000', 'style': 'display: inline-block;'}),
        }
        labels = {
            'phone_number': '',
            'DELETE': 'Remover'
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'idade', 'user_img']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control custom-form-width', 'placeholder': 'Insira seu nome de usuário'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control custom-form-width', 'placeholder': 'Insira sua idade', 'required': 'required'}),
            'user_img': forms.ClearableFileInput(attrs={'class': 'form-control custom-form-width'}),
        }
        labels = {
            'username': 'Nome de usuário',
            'idade': 'Idade',
            'user_img': 'Imagem de perfil',
        }
        
    def clean_idade(self):
        idade = self.cleaned_data['idade']
        if idade:
            if idade < 13:
                self.add_error('idade', 'Menores de 13 anos não podem se cadastrar.')
            else:
                return idade
        else:
            self.add_error('idade', 'É necessário informar a idade.')
