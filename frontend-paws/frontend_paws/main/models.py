from django.db import models
from django.conf import settings

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pets")

    def __str__(self):
        return self.name

    class Meta:

        unique_together = ('user', 'name')
        ordering = ['name']

class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateTimeField()
    reason = models.TextField()

    def __str__(self):
        return f"Appointment for {self.pet.name} on {self.date}"

    class Meta:
        ordering = ['date']

    def is_upcoming(self):
        return self.date > models.functions.Now()
    
    def formatted_date(self):
        return self.date.strftime("%m/%d/%Y %I:%M %p")
