from django.urls import path
from .views import addTrainer
urlpatterns = [
    path('trainer_view/', addTrainer, name="add_trainer")
]