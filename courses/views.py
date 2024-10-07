from django.shortcuts import render
from rest_framework.views import APIView
from customer.models import Customer
from .models import Trainer, Category
from adminuse.models import AddTrainers
from django.http import JsonResponse
from django.views.generic import TemplateView
# Create your views here.
def trainer(request):
    return render(request, 'courses/trainer.html',{"currentUser":request.session['user_name'],'currentEmail':request.session['customer_email'],'currentUserId':request.session['customer_id']})
class CreateTrainer(APIView):
    def post(self, request):
        user_id= request.POST.get('user')
        trainer_name = request.POST.get('trainer_name')
        bio = request.POST.get('bio')
        expertise = request.POST.get('expertise')
        trainer_email = request.POST.get('trainer_email')
        user = Customer.objects.get(customer_id = user_id)
        train = Trainer()
        train.Customer = user
        train.name = trainer_name
        train.bio = bio
        train.expertise = expertise
        train.contact_email = trainer_email
        train.save()
        return JsonResponse({"status":"pass"})
def category(request):
    return render(request, 'courses/add_course_categories.html')

class CreateCategory(APIView):
    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        cat = Category()
        cat.name = name
        cat.description = description
        cat.save()
        return JsonResponse({"status":"pass"})
class ViewCategory(TemplateView):
    template_name = 'courses/add_courses.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        trainers = AddTrainers.objects.all()
        context['trainers'] = trainers
        context['categories'] = categories
        return context
class AddTrainer(APIView):
    def post(self, request):
            tname = request.POST.get('tname')
            tdesc = request.POST.get('tdesc')
            tbio = request.POST.get('tbio')
            texpertise = request.POST.get('texpertise')
            temail = request.POST.get('temail')
            tphone = request.POST.get('tphone')
            taddress = request.POST.get('taddress')
            addtrainer = AddTrainers()
            addtrainer.trainer_name = tname
            addtrainer.trainer_description = tdesc
            addtrainer.trainer_bio = tbio
            addtrainer.trainer_expertise = texpertise
            addtrainer.trainer_email = temail
            addtrainer.trainer_phone = tphone
            addtrainer.trainer_address = taddress
            addtrainer.save()
            return JsonResponse({"status":"pass"})
