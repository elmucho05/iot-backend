from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.core.exceptions import ValidationError



class User(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

# ✅ Base compartment model (Abstract, NOT a database table)
class BaseCompartment(models.Model):
    medicine_name       = models.CharField(max_length=200)
    number_of_medicines = models.IntegerField()
    to_be_repeated      = models.BooleanField(default=False)
    orario_medicina     = models.TimeField(null=True, blank=True)
    orario_mattina      = models.TimeField(null=True, blank=True)
    orario_pomeriggio   = models.TimeField(null=True, blank=True)
    orario_sera         = models.TimeField(null=True, blank=True)

    class Meta:
        abstract = True  # ✅ Prevents Django from creating a table for this

    def clean(self):
        """Validate logic before saving"""
        if self.to_be_repeated:
            # Ensure at least one intake time is set
            if not (self.orario_mattina or self.orario_pomeriggio or self.orario_sera):
                raise ValidationError("At least one of 'orario_mattina', 'orario_pomeriggio', or 'orario_sera' must be set when 'to_be_repeated' is True.")

            # Ensure 'orario_medicina' is empty
            if self.orario_medicina:
                raise ValidationError("'orario_medicina' must be empty when 'to_be_repeated' is True.")
        else:
            # Ensure only 'orario_medicina' is set, and other times are empty
            if not self.orario_medicina:
                raise ValidationError("'orario_medicina' must be set when 'to_be_repeated' is False.")
            if self.orario_mattina or self.orario_pomeriggio or self.orario_sera:
                raise ValidationError("'orario_mattina', 'orario_pomeriggio', and 'orario_sera' must be empty when 'to_be_repeated' is False.")

    def save(self, *args, **kwargs):
        """Auto-generate intake records when a repeated medicine is added"""
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)  # Save the medicine first

        if self.to_be_repeated:
            # ✅ Delete old intakes to avoid duplicates
            from .models import CompartmentIntake  # Prevent circular import
            CompartmentIntake.objects.filter(
                compartment_type=ContentType.objects.get_for_model(self.__class__),
                compartment_id=self.id
            ).delete()

            # ✅ Generate new intakes for each scheduled time
            intake_times = [self.orario_mattina, self.orario_pomeriggio, self.orario_sera]
            for time in intake_times:
                if time:
                    CompartmentIntake.objects.create(
                        compartment_type=ContentType.objects.get_for_model(self.__class__),
                        compartment_id=self.id,
                        intake_time=time
                    )

    def __str__(self):
        return f"{self.medicine_name} ({'Repeated' if self.to_be_repeated else 'Single'})"


# ✅ Concrete Compartment Models (Database Tables)
class Compartment1(BaseCompartment):
    compartment_id = 1


class Compartment2(BaseCompartment):
    compartment_id = 2
class Compartment3(BaseCompartment):
    compartment_id = 3

# ✅ Medicine Intake Model (Now Supports All Compartments)
class CompartmentIntake(models.Model):
    # 🔹 Generic ForeignKey: Can relate to Compartment1, Compartment2, or Compartment3
    compartment_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    compartment_id = models.PositiveIntegerField()
    compartment = GenericForeignKey('compartment_type', 'compartment_id')

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
