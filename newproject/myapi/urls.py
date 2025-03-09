from django.urls import path
from . import views

urlpatterns = [
    # User Endpoints
    # Medicine Endpoints for Multiple Compartments
    path("medicines/<int:compartment_id>/", views.get_medicines, name="get_medicines"),
    path("medicines/<int:compartment_id>/create/", views.create_medicine, name="create_medicine"),
    path("medicines/<int:compartment_id>/<int:pk>/", views.medicine_detail, name="medicine_detail"),

    # Medicine Intake Endpoints
    path("medicines/intakes/pending/", views.get_pending_intakes, name="get_pending_intakes"),
    path("medicines/intakes/taken/", views.get_taken_intakes, name="get_taken_intakes"),
    #path("medicines/intakes/<int:intake_id>/take/", views.mark_intake_as_taken, name="mark_intake_as_taken"),
    path("medicines/intakes/<int:comp_id>/take/", views.take_medicine_from_compartment, name="take_medicine_from_compartment"),

    path("medicines/intakes/<int:comp_id>/pending/", views.get_pending_intakes_by_compartment, name="get_pending_intakes_by_compartment"),
    path("medicines/intakes/<int:comp_id>/taken/", views.get_taken_intakes_by_compartment, name="get_taken_intakes_by_compartment"),

]
