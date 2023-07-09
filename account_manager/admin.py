from django.contrib import admin
from .models import PhoneNumber, User

# Register your models here.
admin.site.register(PhoneNumber)
admin.site.register(User)
