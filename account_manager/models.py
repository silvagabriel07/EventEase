from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator


phone_number_validators = RegexValidator(
        regex=r'^\+\d{2} \d{5}-\d{4}$',
        message="O número de telefone deve estar em um formato válido."
    )


# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, username, **extra_fields):
        print(extra_fields)
        if not email:
            raise ValueError("O endereço de e-mail deve ser informado.")
        email = self.normalize_email(email)
        if not username:
            username = email
        if not password:
            raise ValueError("A senha deve ser informada")

        user = self.model(email=email, username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(email=email, username=username, password=password, **extra_fields)

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email=email, password=password, username=username, **extra_fields)


class User(AbstractUser):
    last_name = first_name = None
    is_active = models.BooleanField(default=False)

    username = models.CharField(max_length=60, unique=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    idade = models.IntegerField(default=None, blank=True, null=True)
    user_img = models.FileField(upload_to='user_img', default='/user_img/user_img.png')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['idade']

    def is_minor(self):
        if self.idade < 18:
            return True
        else:
            return False
        

    def is_user_participant(self, event_instance):
        return event_instance.participants.filter(id=self.id).exists()
    
    def user_already_solicitated(self, event_instance):
        return self.solicitation_set.filter(event=event_instance.id).exists()

    def __str__(self):
        return self.username


class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, validators=[phone_number_validators])