from django.contrib import admin
from .models import  User,BaseCompartment,Compartment1,Compartment2,Compartment3, CompartmentIntake
# Register your models here.
admin.register(User)
#admin.site.register(BaseCompartment)
admin.site.register(Compartment1)
admin.site.register(Compartment2)
admin.site.register(Compartment3)
admin.site.register(CompartmentIntake)