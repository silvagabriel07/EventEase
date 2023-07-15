from django import forms
import re
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import Category

class CustomDateTimeField(forms.DateTimeField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            return datetime.strptime(value, '%d-%m-%Y %H:%M')
        except (ValueError, TypeError):
            raise forms.ValidationError('Informe a data e hora no formato solicitado: DD-MM-AAAA HH:MM')


class CreateEventForm(forms.Form):
    title = forms.CharField(required=True, label='Título:', max_length=40, widget=forms.TextInput(attrs={'id': 'title', 'class':'form-control', 'aria-describedby':'emailHelp'}))
    description = forms.CharField(required=True, label="Descrição:", widget=forms.Textarea(attrs={'id': 'description','class': 'form-control', 'style': 'height: 100px'}))
    # category = forms.MultipleChoiceField(label='Selecione as categorias:', choices=CATEGORIES, widget=forms.SelectMultiple(attrs={'class': 'form-control custom-form-width'}))
    category = forms.ModelChoiceField(label='Selecione a categoria:', queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control custom-form-width'}))
    private = forms.BooleanField(required=False, label='Privado:',widget=forms.CheckboxInput(attrs={'id': 'private','class': 'form-check-label'}))
    free = forms.BooleanField(required=False, label='Para todas as idades:',widget=forms.CheckboxInput(attrs={'id': 'free','class': 'form-check-label'}))
    start_date_time = CustomDateTimeField(required=True, label='Data e hora de início:', input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateTimeInput(attrs={'id': 'start_date_time', 'class': 'form-control custom-form-width', 'placeholder': 'DD-MM-AAAA HH:MM'}))
    final_date_time = CustomDateTimeField(required=True, label='Data e hora de término:', input_formats=['%d/%m/%Y %H:%M'],widget=forms.DateTimeInput(attrs={'id': 'final_date_time', 'class': 'form-control custom-form-width', 'placeholder': 'DD-MM-AAAA HH:MM'}))
    event_banner = forms.FileField(required=False, label='Banner do evento:', widget=forms.FileInput(attrs={'id': 'event_banner', 'class': 'form-control'}))

    def clean_category(self):
        category = self.cleaned_data['category']
        if category:
            if len(category) > 10:
                self.add_error('category', 'Não é possível atribuir mais de 10 categorias ao evento.')
            else:
                return category
        
    def clean_event_banner(self):
        event_banner = self.cleaned_data['event_banner']
        if not event_banner:
            event_banner = '/event_banners/default_event_banner.png'
        return event_banner
        
    def clean(self):
        data_atual = datetime.now()
        start_date_time = self.cleaned_data.get('start_date_time')
        final_date_time = self.cleaned_data.get('final_date_time')
        print(start_date_time, final_date_time)
        if start_date_time and final_date_time:
            if start_date_time > final_date_time:   
                raise ValidationError('Data inicial não pode ser após a data final do evento.')
            if start_date_time < data_atual or final_date_time < data_atual:
                raise ValidationError('Data informada já passou já passou.')