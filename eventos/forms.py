from django import forms

# Descrição: 
 #               <textarea class="form-control" id="floatingTextarea2" style="height: 100px" name="description" required></textarea>


class CreatEventForm(forms.Form):
    title = forms.CharField(required=True, label='Título:', max_length=40, widget=forms.TextInput(attrs={'id': 'title', 'class':'form-control', 'aria-describedby':'emailHelp'}))
    description = forms.CharField(required=False, label="Descrição:", widget=forms.Textarea(attrs={'id': 'description','class': 'form-control', 'style': 'height: 100px'}))
    CATEGORIES = (
        ('birthday', 'Aniversário'),
        ('category_a', 'Categoria A'),
        ('category_b', 'Categoria B'),
        ('category_c', 'Categoria C'),
    )
    category = forms.MultipleChoiceField(label='category', choices=CATEGORIES).widget_attrs('class', 'form-control')
    private = forms.BooleanField(required=False)
    free = forms.BooleanField(required=False)
    start_date_time = forms.DateTimeField()
    final_date_time = forms.DateTimeField()
    event_banner = forms.FileField()
