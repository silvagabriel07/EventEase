from django.db import models
from account_manager.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone as zone
from django_resized import ResizedImageField
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
    start_date_time = models.DateTimeField(default=zone.now)
    final_date_time = models.DateTimeField(default=zone.now)
    event_banner = ResizedImageField(size=[600, 600], quality=85, upload_to='event_banners', default='/default_event_banner.png')
    
    banned_users = models.ManyToManyField(User, related_name='banned_events', blank=True)
    
    def ban_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            self.banned_users.add(user)
            return True
        except ObjectDoesNotExist:
            return False        
    
    def unban_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            self.banned_users.remove(user)
            return True
        except ObjectDoesNotExist:
            return False        
    
    def is_banned_user(self, user_id):
        try:
            return self.banned_users.filter(id=user_id).exists()
        except ObjectDoesNotExist:
            return False
    
    @property
    def qtd_solicitations(self):
        return self.solicitation_set.filter(status='w').count()
    
    @property
    def qtd_participants(self):
        return self.participants.all().count()

    def has_passed(self):
        return self.final_date_time < zone.now()

    def accept_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            solicitation = self.solicitation_set.get(user_id=user_id)
            solicitation.status = 'a'
            solicitation.save()
            self.participants.add(user)
            return True
        except ObjectDoesNotExist:
            return False
        
    def reject_user(self, user_id):
        try:
            solicitation = self.solicitation_set.get(user_id=user_id)
            solicitation.status = 'r'
            solicitation.save()

            return True
        except ObjectDoesNotExist:
            return False
    
    def remove_user(self, participant_id):
        try:
            user = User.objects.get(id=participant_id)
            self.participants.remove(user)
            
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
        return (f'u: {self.user} | e: {self.event} | s: {self.status}')
