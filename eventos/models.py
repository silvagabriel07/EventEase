from django.db import models
from django.db.models import Count
from account_manager.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='event_participants', blank=True)

    requests = models.ManyToManyField(User, related_name='user_requests', blank=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  
    private = models.BooleanField(help_text='definir como True torna preciso a aceitação da requisição de participação')
    free = models.BooleanField(help_text='definir como True significa que é um evento livre, sem restrição de idade')
    start_date_time = models.DateTimeField()
    final_date_time = models.DateTimeField()
    event_banner = models.FileField(upload_to='event_banners', default='default_event_banner.png')

    def count_participants(self):
        return self.participants.count()

    def __str__(self):
        return self.title


class Request(models.Model):
    STATUS = (
        ('a', 'Aceito'),
        ('w', 'Aguardando'),
        ('r', 'Rejeitado')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS, default='w')

    class Meta:
        unique_together = ('user', 'event')
