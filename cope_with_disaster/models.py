from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Is the user allowed to have access to the admin',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text= 'Is the user account currently active',
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Variable(models.Model):
    name = models.CharField(max_length=50, default='var')
    info = models.TextField(default='info')

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12)
    verified = models.BooleanField(default=False)
    lon = models.DecimalField(verbose_name='Longitude',max_digits=9,decimal_places=6)
    lat = models.DecimalField(verbose_name='Latitude',max_digits=9,decimal_places=6)

    def __str__(self):
        return self.email


class Rescuer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Rescuer',
                                verbose_name='User ID')
    name = models.CharField(max_length=50, default='dummy', verbose_name='Volunteer/Organisation Name')
    phone = models.CharField(default='8102071481', max_length=12)
    verified = models.BooleanField(default=False)
    lon = models.DecimalField(default='82.00000',verbose_name='Longitude',max_digits=9,decimal_places=6)
    lat = models.DecimalField(default='27.00000',verbose_name='Latitude',max_digits=9,decimal_places=6)

    def __str__(self):
        return self.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Rescuer(user=instance)
        profile.save()