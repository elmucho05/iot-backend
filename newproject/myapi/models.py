from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class User(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Compartment1(models.Model):
    medicine_name       = models.CharField(max_length=200)
    number_of_medicines = models.IntegerField()
    to_be_repeated      = models.BooleanField(default=False)
    orario_medicina     = models.TimeField(null=True, blank=True)  # Only if not repeated
    orario_mattina      = models.TimeField(null=True, blank=True)
    orario_pomeriggio   = models.TimeField(null=True, blank=True)
    orario_sera         = models.TimeField(null=True, blank=True)

    def clean(self):
        """Validate logic before saving"""
        if self.to_be_repeated:
            if not (self.orario_mattina or self.orario_pomeriggio or self.orario_sera):
                raise ValidationError("At least one of 'orario_mattina', 'orario_pomeriggio', or 'orario_sera' must be set when 'to_be_repeated' is True.")
            if self.orario_medicina:
                raise ValidationError("'orario_medicina' must be empty when 'to_be_repeated' is True.")
        else:
            if not self.orario_medicina:
                raise ValidationError("'orario_medicina' must be set when 'to_be_repeated' is False.")
            if self.orario_mattina or self.orario_pomeriggio or self.orario_sera:
                raise ValidationError("'orario_mattina', 'orario_pomeriggio', and 'orario_sera' must be empty when 'to_be_repeated' is False.")

    def save(self, *args, **kwargs):
        """Auto-generate intake records when a repeated medicine is added"""
        super().save(*args, **kwargs)  # Save the medicine first

        if self.to_be_repeated:
            # ✅ Delete existing intakes to avoid duplicates
            self.intakes.all().delete()  # Now this works!

            # ✅ Generate new intake records for each scheduled time
            if self.orario_mattina:
                CompartmentIntake.objects.create(compartment=self, intake_time=self.orario_mattina)
            if self.orario_pomeriggio:
                CompartmentIntake.objects.create(compartment=self, intake_time=self.orario_pomeriggio)
            if self.orario_sera:
                CompartmentIntake.objects.create(compartment=self, intake_time=self.orario_sera)


    def __str__(self):
        return f"{self.medicine_name} ({'Repeated' if self.to_be_repeated else 'Single'})"


# ✅ New model to track individual medicine intakes
class CompartmentIntake(models.Model):
    compartment = models.ForeignKey(Compartment1, on_delete=models.CASCADE, related_name="intakes")
    intake_time = models.TimeField()
    taken       = models.BooleanField(default=False)
    taken_time  = models.DateTimeField(null=True, blank=True)

    def mark_as_taken(self):
        """Mark this intake as taken and log the time."""
        self.taken = True
        self.taken_time = now()
        self.save()

    def __str__(self):
        return f"{self.compartment.medicine_name} at {self.intake_time} - {'Taken' if self.taken else 'Pending'}"
