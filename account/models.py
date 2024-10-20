from django.db import models

class Account(models.Model):
    group = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name