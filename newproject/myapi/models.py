from django.db import models
from django.core.exceptions import ValidationError


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

    def clean(self):
        """Validate the logic before saving"""
        if self.to_be_repeated:
            # If medicine is to be repeated, at least one of the three time slots must be set
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

    def save(self, *args, **kwargs):
        """Run clean() before saving"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine_name} ({self.number_of_medicines})"