from django import forms
from datetime import datetime
from .models import Category, Event

class CustomDateTimeField(forms.DateTimeField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            return datetime.strptime(value, '%d-%m-%Y %H:%M')
        except (ValueError, TypeError):
            raise forms.ValidationError('Informe a data e hora no formato solicitado: DD-MM-AAAA HH:MM')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'private', 'free', 'start_date_time', 'final_date_time', 'event_banner']

    title = forms.CharField(required=True, label='Título:', max_length=40, widget=forms.TextInput(attrs={'id': 'title', 'class':'form-control', 'aria-describedby':'emailHelp'}))
    description = forms.CharField(required=True, label="Descrição:", widget=forms.Textarea(attrs={'id': 'description','class': 'form-control', 'style': 'height: 100px'}))
    category = forms.ModelChoiceField(required=True, label='Selecione a categoria do evento:', empty_label='Selecione', queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control custom-form-width'}))
    private = forms.BooleanField(required=False, label='Privado:',widget=forms.CheckboxInput(attrs={'id': 'private','class': 'form-check-label'}))
    free = forms.BooleanField(required=False, label='Para todas as idades:',widget=forms.CheckboxInput(attrs={'id': 'free','class': 'form-check-label'}))
    start_date_time = CustomDateTimeField(required=True, label='Data e hora de início:', input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateTimeInput(attrs={'id': 'start_date_time', 'class': 'form-control custom-form-width', 'placeholder': 'DD-MM-AAAA HH:MM'}))
    final_date_time = CustomDateTimeField(required=True, label='Data e hora de término:', input_formats=['%d/%m/%Y %H:%M'],widget=forms.DateTimeInput(attrs={'id': 'final_date_time', 'class': 'form-control custom-form-width', 'placeholder': 'DD-MM-AAAA HH:MM'}))
    event_banner = forms.FileField(required=False, label='Banner do evento:', widget=forms.FileInput(attrs={'id': 'event_banner', 'class': 'form-control'}))

    def clean_event_banner(self):
        event_banner = self.cleaned_data['event_banner']
        if not event_banner:
            event_banner = '/event_banners/default_event_banner.png'
        return event_banner

    def clean(self):
        data_atual = datetime.now()
        start_date_time = self.cleaned_data.get('start_date_time')
        final_date_time = self.cleaned_data.get('final_date_time')
        if start_date_time and final_date_time:
            if start_date_time > final_date_time:
                raise forms.ValidationError('Data inicial não pode ser após a data final do evento.')
            if start_date_time < data_atual or final_date_time < data_atual:
                raise forms.ValidationError('Data informada já passou.')
            if start_date_time == final_date_time:
                raise forms.ValidationError('O evento termina e começa no mesmo momento.')



