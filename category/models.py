from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return self.title