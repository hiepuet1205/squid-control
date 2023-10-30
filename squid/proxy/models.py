from django.db import models

# Create your models here.


class Proxy(models.Model):
    username = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    bandwidth = models.IntegerField(default=2000000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
