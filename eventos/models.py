from django.db import models
from django.db.models import Count
from account_manager.models import User
from django.core.exceptions import ObjectDoesNotExist

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

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  
    private = models.BooleanField(help_text='definir como True torna preciso a aceitação da requisição de participação')
    free = models.BooleanField(help_text='definir como True significa que é um evento livre, sem restrição de idade')
    start_date_time = models.DateTimeField()
    final_date_time = models.DateTimeField()
    event_banner = models.FileField(upload_to='event_banners', default='default_event_banner.png')
    
    def qtd_participants(self):
        return self.participants.count()

    def accept_user(self, user):
        try:
            solicitation = self.solicitation_set.get(user)
            solicitation.status = 'a'
            event = self.participants.add(user)
            event.save()
            return True
        except ObjectDoesNotExist:
            return False
        

    def __str__(self):
        return self.title


class Solicitation(models.Model):
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

    
    def __str__(self) -> str:
        return (f'u: {self.user}-e: {self.event}-s: {self.status}')
