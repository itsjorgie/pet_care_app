from rest_framework import serializers
from .models import Pet, Appointment

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 'user']

class AppointmentSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    pet_species = serializers.CharField(source='pet.species', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'pet', 'pet_name', 'pet_species', 'date', 'reason']