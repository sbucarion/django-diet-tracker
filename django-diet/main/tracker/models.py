from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Log(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    calorie = models.PositiveIntegerField()
    protein = models.PositiveIntegerField()
    fats = models.PositiveIntegerField()
    carbs = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    time_created = models.DateTimeField(auto_now_add=True)