from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


# Create your models here.
class User(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=100)
    #surname = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

    
class Compartment1(models.Model):
    medicine_name       = models.CharField(max_length=200)
    number_of_medicines = models.IntegerField()
    to_be_repeated      = models.BooleanField(default=False)  # No `required=False` needed in models
    orario_medicina     = models.TimeField(null=True, blank=True)  # Allowed to be null/blank
    orario_mattina      = models.TimeField(null=True, blank=True)
    orario_pomeriggio   = models.TimeField(null=True, blank=True)
    orario_sera         = models.TimeField(null=True, blank=True)

    taken               = models.BooleanField(default=False)  # True if the medicine has been taken
    taken_time          = models.DateTimeField(null=True, blank=True)  # Time when the medicine was taken

    def clean(self):
        """Validate logic before saving"""
        if self.to_be_repeated:
            # If medicine is to be repeated, at least one time slot must be set
            if not (self.orario_mattina or self.orario_pomeriggio or self.orario_sera):
                raise ValidationError("At least one of 'orario_mattina', 'orario_pomeriggio', or 'orario_sera' must be set when 'to_be_repeated' is True.")

            # Ensure 'orario_medicina' is not set
            if self.orario_medicina:
                raise ValidationError("'orario_medicina' must be empty when 'to_be_repeated' is True.")

        else:
            # If not repeated, 'orario_medicina' must be set
            if not self.orario_medicina:
                raise ValidationError("'orario_medicina' must be set when 'to_be_repeated' is False.")

            # Ensure no periodic times are set
            if self.orario_mattina or self.orario_pomeriggio or self.orario_sera:
                raise ValidationError("'orario_mattina', 'orario_pomeriggio', and 'orario_sera' must be empty when 'to_be_repeated' is False.")

        # ✅ Ensure taken_time is only set if taken is True
        if self.taken and not self.taken_time:
            self.taken_time = now()  # Auto-assign the current time

        if not self.taken and self.taken_time is not None:
            raise ValidationError("'taken_time' must be empty if 'taken' is False.")

    def save(self, *args, **kwargs):
        """Auto-set taken_time when marked as taken"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine_name} ({'Taken' if self.taken else 'Not Taken'})"
    
# /medicines/comp1/taken -->

# class Comp1History(models.Models):
#     compid = Fo
#     taken = Boolean
#     takne_time = 
class CompartmentHistory(models.Model):
    compartment = models.ForeignKey(Compartment1, on_delete=models.CASCADE, related_name="history")
    taken       = models.BooleanField(default=False)  # Was the medicine taken?
    taken_time  = models.DateTimeField(default=now)   # When was it taken?

    def __str__(self):
        return f"Compartment {self.compartment.id} - {'Taken' if self.taken else 'Not Taken'} at {self.taken_time}"


