from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

PRIORITY_CHOICES=[
    ("High","High"),
    ("Medium","Medium"),
    ("Low","Low"),
]

CATEGORY_CHOICES=[
    ("Study","Study"),
    ("Work","Work"),
    ("Personal","Personal"),
    ("Project","Project"),
    ("Other","Other"),
]

class Task(models.Model):
    user= models.ForeignKey(User,  on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    completed=models.BooleanField(default=False)
    due_date=models.DateField(null=True, blank=True)
    priority= models.CharField(choices=PRIORITY_CHOICES,default="Medium")
    category= models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Other")
    completed_at= models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.title