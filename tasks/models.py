from django.db import models

PRIORITY_CHOICES=[
    ("Low","Low"),
    ("Medium","Medium"),
    ("High","High"),
]

CATEGORY_CHOICES=[
    ("Study","Study"),
    ("Work","Work"),
    ("Personal","Personal"),
    ("Project","Project"),
    ("Other","Other"),
]

class Task(models.Model):
    title=models.CharField(max_length=200)
    completed=models.BooleanField(default=False)
    due_date=models.DateField(null=True, blank=True)
    priority= models.CharField(max_length=10, choices=PRIORITY_CHOICES,default="Medium")
    category= models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Other")
    def __str__(self):
        return self.title