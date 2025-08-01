from django.db import models
from datetime import timedelta

class client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField()
    joining_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)  # NEW FIELD

    def __str__(self):
        return self.name

    @property
    def is_expired(self):
        """Check if client subscription is expired"""
        if self.due_date:
            return self.due_date < models.DateField().to_python(str(models.DateField().get_prep_value(self.due_date)))
        return False


class workoutplan(models.Model):
    client = models.ForeignKey(client, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    plan_description = models.CharField(max_length=200)
    duration_weeks = models.IntegerField()
    goals = models.TextField()

    def __str__(self):
        return f"{self.plan_name} ({self.client.name})"


class progress_tracker(models.Model):
    client = models.ForeignKey(client, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)
    notes = models.TextField()

    def __str__(self):
        return f"{self.client.name} - {self.date}"
