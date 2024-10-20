from django.db import models


class Income(models.Model):
    text = models.CharField(max_length=255)
    amount = models.IntegerField(default=255)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return super().__str__()