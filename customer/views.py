from typing import Any
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Customer
from courses.models import Category, Course
from jobportal.models import CompanyProfile
from adminuse.models import AddTrainers
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.generic.base import TemplateView
from django.conf import settings
# Create your views here.
def signup(request):
    return render(request, 'customer/signup.html')
def login(request):
    return render(request, 'customer/login.html')
def logout(request):
    request.session.pop('user_name',None)
    request.session.pop('customer_email',None)
    request.session.pop('customer_id',None)
    return redirect('login')
def index2(request):
    domains = Category.objects.all()
    allTrainers = AddTrainers.objects.all().order_by('-trainer_created')
    courses = Course.objects.all()
    return render(request, 'customer/index-3.html',{'currentUser':request.session.get('user_name',''),'domains':domains,'allTrainers':allTrainers,"courses":courses})
def courses(request):
    domains = Category.objects.all()
    allTrainers = AddTrainers.objects.all().order_by('-trainer_created')
    courses = Course.objects.all()
    return render(request, 'courses/courses.html',{'currentUserId':request.session['customer_id'],'currentUser':request.session.get('user_name',''),'domains':domains,'allTrainers':allTrainers,"courses":courses})

def aboutus(request):
    domains = Category.objects.all()
    allTrainers = AddTrainers.objects.all().order_by('-trainer_created')
    courses = Course.objects.all()
    return render(request, 'customer/about-01.html',{'currentUser':request.session.get('user_name',''),'domains':domains,'allTrainers':allTrainers,"courses":courses})
def index2(request):
    domains = Category.objects.all()
    allTrainers = AddTrainers.objects.all().order_by('-trainer_created')
    courses = Course.objects.all()
    return render(request, 'customer/index-3.html',{'currentUser':request.session.get('user_name',''),'domains':domains,'allTrainers':allTrainers,"courses":courses})
def index2(request):
    domains = Category.objects.all()
    allTrainers = AddTrainers.objects.all().order_by('-trainer_created')
    courses = Course.objects.all()
    return render(request, 'customer/index-3.html',{'currentUser':request.session.get('user_name',''),'domains':domains,'allTrainers':allTrainers,"courses":courses})
def privacy(request):
    return render(request, 'customer/privacy.html')
def contactus(request):
    return render(request, 'customer/contact-01.html')
def refund(request):
    return render(request, 'customer/refund.html')
class CreateUser(APIView):
    def post(self, request):
        name = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if Customer.objects.filter(email = email).exists():
            return JsonResponse({'status':"fail","message":"Email Already Exists"})
        customer = Customer()
        customer.username = name
        customer.email = email
        customer.phone = phone
        customer.password = password
        customer.save()
        return JsonResponse({"status":"pass"})
def index(request):
    domains = Category.objects.all()
    user_id = request.session['customer_id']
    company_data = CompanyProfile.objects.filter(user_id = user_id)
    allTrainers = AddTrainers.objects.all().order_by('-trainer_created')
    courses = Course.objects.all()
    return render(request, 'customer/index.html',{"currentUser":request.session['user_name'],
                                                  'currentEmail':request.session['customer_email'],
                                                  'currentUserId':request.session['customer_id'],'domains':domains,
                                                  'company_data':company_data,'allTrainers':allTrainers,"courses":courses})
class LoginCheck(APIView):
    def post(self, request):
        email_1 = request.POST['email'] # Using request.data if POST data is sent as JSON
        password_1 = request.POST['password']
        customer = Customer.objects.get(email = email_1)
        try:
            # Query by email or any unique field instead of password
            if Customer.objects.filter(email = email_1, password = password_1).exists():
                request.session['user_name'] = customer.username
                request.session['customer_id'] = customer.customer_id
                request.session['customer_email'] = email_1 
                return JsonResponse({"status":"pass","name":customer.username,'cid':customer.customer_id,"role":customer.role,'email':customer.email})
            else:
                 return JsonResponse({"status":"fail", "message":"Invalid Credentials"})
        except Customer.DoesNotExist:
            # Handle case when no customer is found with the provided email
            return JsonResponse({"status": "false", "failure": "Account does not exist Please Signup"})
        return HttpResponse("Success")
    
class ViewCustomer(TemplateView):
    template_name = 'customer/viewcust.html'
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        custdata = Customer.objects.all()
        context['custdata'] = custdata
        return context
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
# Forgot Password View
class ForgotPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            customer = Customer.objects.get(email=email)
            reset_link = f"http://127.0.0.1:9000/reset_password/{customer.customer_id}/"
            
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )
            return JsonResponse({"status": "pass", "message": "Reset link sent!"})
        except Customer.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "Email not found!"})
def reset_password(request, cid):
    customer = Customer.objects.get(customer_id = cid)
    return render(request, 'customer/reset_password.html', {'customer':customer})
class UpdatePassword(APIView):
    def post(self, request):
        id = request.POST.get('id')
        newpassword = request.POST.get('password')
        confpassword = request.POST.get('confirm_password')
        Customer.objects.filter(customer_id = id).update(password = newpassword,confirm_password = confpassword)
        return JsonResponse({"status":"pass"})
def terms_conditions(request):
    return render(request, 'customer/termsconditions.html')