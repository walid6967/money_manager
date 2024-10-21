from django.db import models
from group.models import Group

class Account(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return self.name