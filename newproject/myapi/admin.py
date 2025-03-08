from django.contrib import admin
from .models import  User,Compartment1, CompartmentIntake
# Register your models here.
admin.register(User)
admin.site.register(Compartment1)
admin.site.register(CompartmentIntake)