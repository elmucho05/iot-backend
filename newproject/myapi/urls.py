from django.urls import path
from . import views

app_name = "myapi"
urlpatterns = [
    path("users/", views.get_users, name="get_users"),
    path("users/create/", views.create_user, name="create_user"),
    path("users/<int:pk>", views.user_detail, name="user_detail"),
    path("medicines/create", views.create_medicine, name="create_medicine"),
    path("medicines/", views.get_medicines, name="get_medicines"),
    
]