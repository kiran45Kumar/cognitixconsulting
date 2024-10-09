from django.shortcuts import render
from .models import AddTrainers
from courses.models import Category
# Create your views here.
def addTrainer(request):
    return render(request, 'courses/add_trainer.html')

def adminDashboard(request):
    categories = Category.objects.all()
    return render(request, 'adminuse/admin.html',{'categories':categories})