from django.db import models
from account_manager.models import User
# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='event_participants', blank=True, null=True)

    CATEGORIES = (
        ('birthday', 'Aniversário'),
        ('category_a', 'Categoria A'),
        ('category_b', 'Categoria B'),
        ('category_c', 'Categoria C'),
    )

    category = models.CharField(max_length=15, choices=CATEGORIES)
    private = models.BooleanField(help_text='definir como True torna preciso a aceitação da requisição de participação')
    free = models.BooleanField(help_text='definir como True significa que é um evento livre, sem restrição de idade')
    start_date_time = models.DateTimeField()
    final_date_time = models.DateTimeField()
    # AInda n migrei esse campo
    event_banner = models.FileField(upload_to='event_banners')

    def __str__(self):
        return self.title
