from django.urls import path
from .views import addTrainer,adminDashboard,trainerFunction
urlpatterns = [
    path('trainer_view/', addTrainer, name="add_trainer"),
    path('admin_dashboard/', adminDashboard, name="admin_dashboard"),
    path('view_trainer/<int:id>', trainerFunction, name="trainer_view"),
    
]