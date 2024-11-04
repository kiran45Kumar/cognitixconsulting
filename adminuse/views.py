from django.shortcuts import render
from .models import AddTrainers
from courses.models import Category
from customer.models import Customer
# Create your views here.
def addTrainer(request):
     context = {}
     categories = Category.objects.all()
     user_id = request.session['customer_id']
     trainers = AddTrainers.objects.filter(user_id = user_id)
     customers = Customer.objects.filter(customer_id = user_id)
     context['categories'] = categories
     return render(request, 'courses/add_trainer.html',{'categories':categories,'currentUserId':request.session['customer_id'],'currentUsername':request.session['user_name'],'currentUserEmail':request.session['customer_email'],'customers':customers,"trainers":trainers})

def adminDashboard(request):
    categories = Category.objects.all()
    return render(request, 'adminuse/admin.html',{'categories':categories,'currentUserId':request.session['customer_id'],'currentUsername':request.session['user_name'],'currentUserEmail':request.session['customer_email']})
def trainerFunction(request, id):
    trainer = AddTrainers.objects.get(trainer_id = id)
    return render(request, 'adminuse/trainerview.html',{'trainer':trainer})