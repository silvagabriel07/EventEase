from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_resized import ResizedImageField


phone_number_validators = RegexValidator(
        regex=r'^\+\d{2} \d{5}-\d{4}$',
        message="O número de telefone deve estar em um formato válido."
    )


def password_validate(password):
    if not password:
        raise ValidationError("A senha deve ser informada.")

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError("O endereço de e-mail deve ser informado.")
        email = self.normalize_email(email)
        if not username:
            username = email
        password_validate(password)

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
            raise ValueError("Superuser deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser deve ter is_superuser=True.")

        return self._create_user(email=email, password=password, username=username, **extra_fields)

DEFAULT_USER_IMG = '/user_img/user_img.png'

class User(AbstractUser):
    last_name = first_name = None
    is_active = models.BooleanField(default=False)

    username = models.CharField(max_length=60, unique=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    idade = models.IntegerField(default=None, blank=True, null=True)
    user_img = ResizedImageField(size=[600, 600], quality=85, upload_to='user_img', default=DEFAULT_USER_IMG)

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
    
    def user_already_solicited(self, event_instance):
        return self.solicitation_set.filter(event=event_instance.id).exists()

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.pk is not None: 
            user = User.objects.get(pk=self.pk)
            # Make the email field uneditable
            if user.email != self.email:
                raise ValidationError("O campo 'email' não pode ser alterado.")
        super().save(*args, **kwargs)
        

class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, validators=[phone_number_validators])
    
    def clean(self):
        existing_phone_numbers = PhoneNumber.objects.filter(user=self.user).exclude(id=self.id)
        # If the user is adding a new phone number and already have 3
        if self.id is None and existing_phone_numbers.count() >= 3:
            raise ValidationError('Um usuário só pode ter no máximo 3 números de telefone.')
        elif existing_phone_numbers.count() > 3:
            raise ValidationError('Um usuário só pode ter no máximo 3 números de telefone.')
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

