from django import forms
from .models import CATEGORIES

class CreatEventForm(forms.Form):
    title = forms.CharField(required=True, label='Título:', max_length=40, widget=forms.TextInput(attrs={'id': 'title', 'class':'form-control', 'aria-describedby':'emailHelp'}))
    description = forms.CharField(required=False, label="Descrição:", widget=forms.Textarea(attrs={'id': 'description','class': 'form-control', 'style': 'height: 100px'}))
    category = forms.MultipleChoiceField(label='Selecione as categorias:', choices=CATEGORIES, widget=forms.SelectMultiple(attrs={'class': 'form-control custom-form-width'}))
    private = forms.BooleanField(required=False, label='Para todas as idades:',widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}))
    free = forms.BooleanField(required=False, label='Privado:',widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}))
    start_date_time = forms.DateTimeField(required=True, label='Data e hora de início:', widget=forms.DateTimeInput(attrs={'class': 'form-control custom-form-width', 'placeholder': 'YYYY-MM-DD HH:MM'}))
    final_date_time = forms.DateTimeField(required=True, label='Data e hora de término:', widget=forms.DateTimeInput(attrs={'class': 'form-control custom-form-width', 'placeholder': 'YYYY-MM-DD HH:MM'}))
    event_banner = forms.FileField(required=False, label='Banner do evento:', widget=forms.FileInput(attrs={'class': 'form-control'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            pass
        # validações