from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, username=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError("O indereço de e-mail deve ser informado.")
        email = self.normalize_email(email)
        if not username:
            username = email
        if phone_number:
            phone_number =  phone_number.replace('-', '').replace(' ', '')
            for num in phone_number[1:]:
                if not num.isdigit():
                    raise ValueError("Número de telefone inválido.")

        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, phone_number=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(email=email, username=username, password=password, phone_number=phone_number **extra_fields)


class User(AbstractUser):
    last_name = first_name = None
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=60, validators=[username_validator], unique=False)
    email = models.EmailField(max_length=254, unique=True)
    idade = models.IntegerField()

    objects = CustomUserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.username


class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number_validators = RegexValidator(
        regex=r'^\+\d{2}\d{2}\d{4}\d{4}$',
        message="O número de telefone deve estar em um formato válido."
    )
    phone_number = models.CharField(max_length=15, validators=phone_number_validators,  default=None)