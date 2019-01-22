from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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