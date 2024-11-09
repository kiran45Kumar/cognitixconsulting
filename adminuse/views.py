from django.shortcuts import render
from .models import AddTrainers, Subscription
from courses.models import Category, Payment
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
     return render(request, 'courses/add_trainer.html',{'categories':categories,'currentUserId':request.session['customer_id'],
                                                        'currentUsername':request.session['user_name'],
                                                        'currentUserEmail':request.session['customer_email'],
                                                        'customers':customers,"trainers":trainers})

def adminDashboard(request):
    categories = Category.objects.all()
    allcompanies = CompanyProfile.objects.all()
    payments = Payment.objects.all()
    
    return render(request, 'adminuse/admin.html',{'categories':categories,
                                                  'currentUserId':request.session['customer_id'],
                                                  'currentUsername':request.session['user_name'],
                                                  'currentUserEmail':request.session['customer_email'],
                                                  'allcompanies':allcompanies,"payments":payments})
def trainerFunction(request, id):
    trainer = AddTrainers.objects.get(trainer_id = id)
    categories = Category.objects.all()
    return render(request, 'adminuse/trainerview.html',{'trainer':trainer,"categories":categories})
def view_all_jobs(request):
    alljobs = PostJob.objects.all()
    categories = Category.objects.all()
    allcompanies = CompanyProfile.objects.all()
    return render(request, 'adminuse/view_all_jobs.html',{'alljobs':alljobs,
                                                          'currentUserId':request.session['customer_id'],
                                                          'currentUsername':request.session['user_name'],
                                                          'currentUserEmail':request.session['customer_email'],
                                                          'allcompanies':allcompanies,
                                                          "categories":categories
                                                          })
def view_all_companies(request):
    allcompanies = CompanyProfile.objects.all()
    categories = Category.objects.all()
    alljobs = PostJob.objects.all()
    return render(request, 'adminuse/view_all_companies.html',{'allcompanies':allcompanies,
                                                               'alljobs':alljobs,
                                                          'currentUserId':request.session['customer_id'],
                                                          'currentUsername':request.session['user_name'],
                                                          'currentUserEmail':request.session['customer_email'],
                                                          "categories":categories})
def view_all_customers(request):
    categories = Category.objects.all()
    allcustomers = Customer.objects.all()
    allcompanies = CompanyProfile.objects.all()
    alljobs = PostJob.objects.all()
    return render(request, 'adminuse/view_all_customers.html',{'allcustomers':allcustomers,'allcompanies':allcompanies,
                                                               'alljobs':alljobs,
                                                          'currentUserId':request.session['customer_id'],
                                                          'currentUsername':request.session['user_name'],
                                                          'currentUserEmail':request.session['customer_email'],
                                                          "categories":categories})
def view_all_messages(request):
    categories = Category.objects.all()
    allcustomers = Customer.objects.all()
    allcompanies = CompanyProfile.objects.all()
    alljobs = PostJob.objects.all()
    payments = Payment.objects.all()
    return render(request, 'adminuse/messages.html',{'allcustomers':allcustomers,'allcompanies':allcompanies,
                                                               'alljobs':alljobs,
                                                          'currentUserId':request.session['customer_id'],
                                                          'currentUsername':request.session['user_name'],
                                                          'currentUserEmail':request.session['customer_email'],
                                                          "categories":categories,"payments":payments})
def view_all_payments(request):
    categories = Category.objects.all()
    allcustomers = Customer.objects.all()
    allcompanies = CompanyProfile.objects.all()
    alljobs = PostJob.objects.all()
    payments = Payment.objects.all()
    return render(request, 'adminuse/messages.html',{'allcustomers':allcustomers,'allcompanies':allcompanies,
                                                               'alljobs':alljobs,
                                                          'currentUserId':request.session['customer_id'],
                                                          'currentUsername':request.session['user_name'],
                                                          'currentUserEmail':request.session['customer_email'],
                                                          "categories":categories,"payments":payments})
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
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView

class UpdateStatus(APIView):
    def post(self, request):
        id = request.POST.get('id')
        status = request.POST.get('status')
        
        # Update the payment status
        payment = Payment.objects.filter(id=id).first()
        if payment:
            payment.status = status
            payment.save()
            
            # Send email if status is confirmed
            if status == 'Confirmed':
                user_email = payment.user.email  # Assuming `user` has an `email` field
                course_name = payment.course.title  # Assuming `course` has a `name` field
                subject = "Payment Confirmation"
                message = f"Dear {payment.user.username},\n\nYour payment for the course '{course_name}' has been confirmed.\nThank you for your purchase!\n\nBest regards,\nYour Team"
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,  # Your email configuration in settings.py
                    [user_email],
                    fail_silently=False,
                )
                
        return JsonResponse({"status": "pass"})

class RejectPayment(APIView):
    def post(self, request):
        id = request.POST.get('id')
        status = request.POST.get('status')
        Payment.objects.filter(id = id).update(status = status)
        return JsonResponse({"status":"pass"})
class RemovePayment(APIView):
    def post(self, request):
        id = request.POST.get('id')
        Payment.objects.filter(id = id).delete()
        return JsonResponse({"status":"pass"})
def subscription_html(request):
    categories = Category.objects.all()
    allcustomers = Customer.objects.all()
    allcompanies = CompanyProfile.objects.all()
    alljobs = PostJob.objects.all()
    payments = Payment.objects.all()
    return render(request, 'adminuse/add_subscription.html',{'allcustomers':allcustomers,'allcompanies':allcompanies,
                                                          'alljobs':alljobs,'currentUserId':request.session['customer_id'],
                                                          'currentUsername':request.session['user_name'],
                                                          'currentUserEmail':request.session['customer_email'],
                                                          "categories":categories,"payments":payments}) 
class AddSubscription(APIView):
    def post(self, request):
        subscription_name = request.POST.get('subscription_name')
        subscription_features = request.POST.get('subscription_features')
        amount = request.POST.get('amount')
        duration = request.POST.get('duration')
        discount = request.POST.get('discount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        max_users = request.POST.get('max_users')
        subscription = Subscription()
        subscription.subscription_name = subscription_name
        subscription.subscription_features = subscription_features
        subscription.amount = amount
        subscription.duration = duration
        subscription.discount = discount
        subscription.start_date = start_date
        subscription.end_date = end_date
        subscription.description = description
        subscription.max_users = max_users
        subscription.save()
        return JsonResponse({"status":"pass"})
def adminDash(request):
    return render(request, 'adminuse/admin_dashboard.html')