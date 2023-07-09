from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator


# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, username=None, **extra_fields):
        if not email:
            raise ValueError("O indereço de e-mail deve ser informado.")
        email = self.normalize_email(email)
        if not username:
            username = email

        # Preciso validar o phonenumber
            
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    last_name = first_name = None
    phone_number_validators = RegexValidator(
        regex=r'^\d{10,15}$',
        message="O número de telefone deve estar em um formato válido."
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=60, validators=[username_validator], unique=False)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=15, validators=phone_number_validators)
    idade = models.IntegerField()

    objects = CustomUserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.username
