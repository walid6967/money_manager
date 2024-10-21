from django.db import models
from category.models import Category


class Income(models.Model):
    text = models.CharField(max_length=255)
    amount = models.IntegerField(default=255)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return self.text