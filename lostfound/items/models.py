from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    contact = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default="Open")

    def __str__(self):
        return self.title