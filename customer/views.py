from django.shortcuts import render
from rest_framework.views import APIView
from .models import Customer
from django.http import JsonResponse
# Create your views here.
def signup(request):
    return render(request, 'customer/signup.html')
def login(request):
    return render(request, 'customer/login.html')

class CreateUser(APIView):
    def post(self, request):
        name = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('cpassword')
        role = request.POST.get('role')
        if Customer.objects.filter(email = email).exists():
            return JsonResponse({'status':"fail","message":"Email Already Exists"})
        customer = Customer()
        customer.username = name
        customer.email = email
        customer.phone = phone
        customer.password = password
        customer.confirm_password = confirmpassword
        customer.role = role
        customer.save()
        return JsonResponse({"status":"pass"})
def index(request):
    return render(request, 'customer/index.html',{"currentUser":request.session['user_name'],'currentEmail':request.session['customer_email']})
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