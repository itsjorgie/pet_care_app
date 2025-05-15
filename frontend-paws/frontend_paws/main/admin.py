from django.contrib import admin
from .models import Pet, Appointment

class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'user')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet', 'date', 'reason')

admin.site.register(Pet, PetAdmin)
admin.site.register(Appointment, AppointmentAdmin)
