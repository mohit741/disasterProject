from django.db import models


class Variable(models.Model):
    name = models.CharField(max_length=50, default='var')
    info = models.TextField(default='info')

    def __str__(self):
        return self.name


class User(models.Model):
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
