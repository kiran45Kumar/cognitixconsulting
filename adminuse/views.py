from django.shortcuts import render
from .models import AddTrainers
from courses.models import Category
from customer.models import Customer
from jobportal.models import PostJob, CompanyProfile
from rest_framework.views import APIView
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
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
    allcompanies = CompanyProfile.objects.all()

    return render(request, 'adminuse/admin.html',{'categories':categories,
                                                  'currentUserId':request.session['customer_id'],
                                                  'currentUsername':request.session['user_name'],
                                                  'currentUserEmail':request.session['customer_email'],
                                                  'allcompanies':allcompanies})
def trainerFunction(request, id):
    trainer = AddTrainers.objects.get(trainer_id = id)
    return render(request, 'adminuse/trainerview.html',{'trainer':trainer})
def view_all_jobs(request):
    alljobs = PostJob.objects.all()
    allcompanies = CompanyProfile.objects.all()
    return render(request, 'adminuse/view_all_jobs.html',{'alljobs':alljobs,
                                                          'currentUserId':request.session['customer_id'],
                                                          'currentUsername':request.session['user_name'],
                                                          'currentUserEmail':request.session['customer_email'],
                                                          'allcompanies':allcompanies
                                                          })
def view_all_companies(request):
    allcompanies = CompanyProfile.objects.all()
    alljobs = PostJob.objects.all()
    return render(request, 'adminuse/view_all_companies.html',{'allcompanies':allcompanies,
                                                               'alljobs':alljobs,
                                                          'currentUserId':request.session['customer_id'],
                                                          'currentUsername':request.session['user_name'],
                                                          'currentUserEmail':request.session['customer_email'],})
def view_all_customers(request):
    allcustomers = Customer.objects.all()
    allcompanies = CompanyProfile.objects.all()
    alljobs = PostJob.objects.all()
    return render(request, 'adminuse/view_all_customers.html',{'allcustomers':allcustomers,'allcompanies':allcompanies,
                                                               'alljobs':alljobs,
                                                          'currentUserId':request.session['customer_id'],
                                                          'currentUsername':request.session['user_name'],
                                                          'currentUserEmail':request.session['customer_email'],})
class DeleteJobs(APIView):
    def post(self, request):
        id = request.POST.get('id')
        PostJob.objects.filter(job_id = id).delete()
        return JsonResponse({"status":"pass"})
class DeleteCompany(APIView):
    def post(self, request):
        id = request.POST.get('id')
        CompanyProfile.objects.filter(company_id = id).delete()
        return JsonResponse({"status":"pass"})
class UpdateUser(APIView):
    def post(self, request):
        id = request.POST.get('id')
        name = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')
        role = request.POST.get('role')
        Customer.objects.filter(customer_id = id).update(username = name, email = email, phone=phone,password=password,confirm_password=confirmpassword,role = role)
        return JsonResponse({"status":"pass"})
class DeleteUser(APIView):
    def post(self, request):
       id = request.POST.get('id')
       Customer.objects.filter(customer_id = id).delete()
       return JsonResponse({"status":"pass"})