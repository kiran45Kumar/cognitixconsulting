from django.shortcuts import render
from .models import AddTrainers
# Create your views here.
def addTrainer(request):
    return render(request, 'courses/add_trainer.html')

