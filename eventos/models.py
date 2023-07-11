from django.db import models

# Create your models here.

class EventCategory(models.Model):
    name = models.CharField(max_length=40)
    
class Event(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    category = models.ManyToManyField('EventCategory')
    free = models.BooleanField()
    start_time = models.DateTimeField()
    start_date = models.DateField()
    final_date = models.DateField()
    final_time = models.DateTimeField()

