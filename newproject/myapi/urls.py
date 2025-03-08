from django.urls import path
from . import views

app_name = "myapi"

urlpatterns = [
    # User Endpoints
    path("users/", views.get_users, name="get_users"),
    path("users/create/", views.create_user, name="create_user"),
    path("users/<int:pk>/", views.user_detail, name="user_detail"),

    # Medicine Endpoints
    path("medicines/", views.get_medicines, name="get_medicines"),
    path("medicines/create/", views.create_medicine, name="create_medicine"),
    path("medicines/<int:pk>/", views.medicine_detail, name="medicine_detail"),
    path("medicines/schedule/", views.get_daily_schedule, name="get_daily_schedule"),
    #path("medicines/<int:pk>/take/", views.mark_as_taken, name="mark_as_taken"),
    path("medicines/intakes/pending/", views.get_pending_intakes, name="get_pending_intakes"),
    path("medicines/intakes/<int:intake_id>/take/", views.mark_intake_as_taken, name="mark_intake_as_taken"),
    path("medicines/intakes/taken/", views.get_taken_intakes, name="get_taken_intakes"),
]

