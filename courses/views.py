from django.shortcuts import render
from rest_framework.views import APIView
from customer.models import Customer
from .models import Trainer, Category,Cart
from adminuse.models import AddTrainers
from django.http import JsonResponse, HttpResponse, Http404
from django.views.generic import TemplateView
from .models import Course,Enrollment, CourseSchedule, Payment
from jobportal.models import CompanyProfile, PostJob
import json
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
    context = {}
    categories = Category.objects.all().order_by('-created_at')
    context['categories'] = categories
    return render(request, 'courses/add_course_categories.html',{'categories':categories,'currentUserId':request.session['customer_id'],'currentUsername':request.session['user_name'],'currentUserEmail':request.session['customer_email']})

class CreateCategory(APIView):
    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        if Category.objects.filter(name = name).exists():
            return JsonResponse({'status':"fail",'message':"Category already exists"})
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
        context['currentUserId'] = self.request.session['customer_id']
        context['currentUsername'] = self.request.session['user_name']
        context['currentUserEmail'] = self.request.session['customer_email']
        return context
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Course, Category, AddTrainers  # Make sure to import your models
import json

class CreateCourses(APIView):
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        gst = request.POST.get('gst')
        total_price = request.POST.get('total_price')
        skillsgained = request.POST.get('skillsgained')
        vid = request.FILES.get('vid')
        img = request.FILES.get('img')
        category_id = request.POST.get('category')
        course_sample_certificate = request.FILES.get("course_sample_certificate")
        course_brochure = request.FILES.get("course_brochure")
        completion_of_days = request.POST.get("completion_of_days")
        completion_of_hrs = request.POST.get("completion_of_hrs")
        sdate = request.POST.get("sdate")
        edate = request.POST.get("edate")
        trainer_ids = json.loads(request.POST.get("trainers", "[]"))

        # Get category 
        cat = Category.objects.get(id=category_id)
        # Create a new Course instance
        course = Course(
            title=title,
            description=description,
            course_gst=gst,
            course_video=vid,
            course_img = img,
            total_price=total_price,
            skillsgain=skillsgained,
            price=price,
            category=cat,
            course_sample_certificate=course_sample_certificate,
            course_brochure=course_brochure,
            completion_of_days=completion_of_days,
            completion_of_hrs=completion_of_hrs,
            start=sdate,
            end=edate,
        )
        course.save()
        for trainer_id in trainer_ids:
            trainer = AddTrainers.objects.get(trainer_id=trainer_id)
            course.trainers.add(trainer)
        return JsonResponse({"status": "pass"})

class UpdateCourses(APIView):
    def post(self, request):
        id= request.POST.get('id')
        title= request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        gst = request.POST.get('course_gst')   
        Course.objects.filter(course_id = id).update(title = title,description = description, price = price, course_gst = gst)
        return JsonResponse({"status":"pass"}) 
class AddTrainer(APIView):
    def post(self, request):
            tname = request.POST.get('tname')
            tdesc = request.POST.get('tdesc')
            tbio = request.POST.get('tbio')
            texpertise = json.loads(request.POST.get('texpertise')) 
            texperience = request.POST.get('texperience')
            timg = request.FILES.get('timg')
            tspec = request.POST.get('tspec')
            user_id = request.POST.get('user_id')
            if AddTrainers.objects.filter(trainer_name = tname).exists():
                return JsonResponse({"status":"fail","message":"Trainer Name Already Exists!"})
            user = Customer.objects.get(customer_id = user_id)
            addtrainer = AddTrainers()
            addtrainer.trainer_name = tname
            addtrainer.trainer_desc = tdesc
            addtrainer.trainer_bio = tbio
            addtrainer.trainer_expertise = texpertise
            addtrainer.trainer_experience = texperience
            addtrainer.trainer_photo = timg
            addtrainer.trainer_specialization = tspec
            addtrainer.user_id = user
            addtrainer.save()
            return JsonResponse({"status":"pass"})
class ViewCourses(TemplateView):
    template_name = 'courses/view_courses.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.all()
        categories = Category.objects.all()
        context['categories'] = categories
        context['courses'] = courses
        context['currentUsername']=self.request.session['user_name']
        context['currentUserEmail']=self.request.session['customer_email']
        return context
class ViewTrainers(TemplateView):
    template_name = 'courses/view_trainer.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainers = AddTrainers.objects.all()
        for trainer in trainers:
            expertise_cleaned = trainer.trainer_expertise.replace('\n', ',').replace('[', '').replace(']', '')
            trainer.expertise_list = [exp.strip() for exp in expertise_cleaned.split(',') if exp.strip()]
        context['trainers'] = trainers
        return context
    
class DeleteCourse(APIView):
    def post(self, request):
       id = request.POST.get('id')
       Course.objects.filter(course_id = id).delete()
       return JsonResponse({"status":"pass"})
    
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db.utils import IntegrityError
from .models import Course, Customer, Enrollment

class Enroll_user(APIView):
    def post(self, request):
        course_id = request.POST.get('course_id')
        customer_id = self.request.session.get('customer_id')

        # Ensure course and customer exist
        try:
            course = Course.objects.get(course_id=course_id)
            customer = Customer.objects.get(customer_id=customer_id)
        except Course.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "Course not found"}, status=404)
        except Customer.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "Customer not found"}, status=404)

        # Check if the user is already enrolled in the course
        if Enrollment.objects.filter(customer=customer, course=course).exists():
            return JsonResponse({"status": "fail", "message": "Already enrolled in this course"}, status=400)

        # Try saving the enrollment, handle any possible IntegrityError
        try:
            enrollmentbyuser = Enrollment(customer=customer, course=course)
            enrollmentbyuser.save()
            return JsonResponse({"status": "pass", "message": "Enrollment successful"}, status=201)
        except IntegrityError:
            return JsonResponse({"status": "fail", "message": "Enrollment failed due to database error"}, status=500)


class CoursesEnrollForUser(TemplateView):
    template_name = 'courses/courseenrolledby.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.request.session.get('customer_id')
        customer_name = self.request.session.get('user_name')
        courses = Course.objects.all()
        context['courses'] = courses 
        context['customer_id'] = customer_id
        context['customer_name'] = customer_name
        return context
def enrolledUsers(request):
    customer_id = request.session.get('customer_id')
    enrolls = Enrollment.objects.filter(customer = customer_id)
    return render(request, 'courses/enrollment.html', {'enrolls':enrolls,'customer_name':request.session.get('user_name')})
def viewCourseById(request, id):
    course_by_id = Course.objects.get(course_id=id)
    domains = Category.objects.all()
    return render(request, 'courses/coursedetails.html',{'course_by_id':course_by_id,"currentUser":request.session.get('user_name',''),'domains':domains})
class ViewAllTrainer(TemplateView):
    template_name = 'courses/trainerview.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        all_trainer = AddTrainers.objects.all().order_by('-trainer_created')
        categories = Category.objects.all()
        context['all_trainers'] = all_trainer
        context['currentUsername']=self.request.session['user_name']
        context['currentUserEmail']=self.request.session['customer_email']
        context['categories']=categories
        return context

class DeleteCategory(APIView):
    def post(self, request):
        id = request.POST['id']
        Category.objects.filter(id = id).delete()
        return JsonResponse({'status':"pass"})
def  schedule(request,id):
    trainer = AddTrainers.objects.get(trainer_id = id)
    categories = Category.objects.all()
    return render(request, 'courses/schedule.html', {'trainer':trainer,'categories':categories,"currentUsername":request.session['user_name'],"currentUserEmail":request.session['customer_email']})
class CreateSchedule(APIView):
    def post(self, request):
        trainer_id = request.POST.get('trainer')
        region =  request.POST.get('region')
        start =  request.POST.get('start')
        end =  request.POST.get('end')
        stime =  request.POST.get('stime')
        etime =  request.POST.get('etime')
        train = AddTrainers.objects.get(trainer_id = trainer_id)
        sched = CourseSchedule()
        sched.trainer = train
        sched.region = region
        sched.start_date = start
        sched.end_date = end
        sched.schedule_start_time = stime
        sched.schedule_end_time = etime
        sched.save()
        return JsonResponse({"status":"pass"})
class VieWScheduleAdmin(TemplateView):
    template_name = 'courses/view_schedules.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('customer_id')
        trainerdata = AddTrainers.objects.filter(user_id = user_id)
        schedule = CourseSchedule.objects.all().order_by('-created_at')
        categories = Category.objects.all()
        context['currentUsername'] = self.request.session.get('user_name')
        context['currentUserEmail'] = self.request.session.get('customer_email')
        context['trainerdata'] = trainerdata
        context['schedules'] = schedule
        context['categories']=categories
        return context
class RemoveScheduleAdmin(APIView):
    def post(self, request):
        id = request.POST['id']
        CourseSchedule.objects.filter(id = id).delete()
        return JsonResponse({'status':"pass"})
    from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Course

def download_brochure(request, course_id):
    # Get the course object
    course = get_object_or_404(Course, course_id=course_id)
    
    # Get the file path
    file_path = course.course_brochure.path

    # Serve the file
    try:
        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{course.title}_brochure.pdf"'
            return response
    except FileNotFoundError:
        raise Http404("File not found.")
# views.py
from django.shortcuts import render
from .models import CourseSchedule, AddTrainers

def trainer_schedule(request, trainer_id):
    trainer = AddTrainers.objects.get(trainer_id=trainer_id)
    schedules = CourseSchedule.objects.filter(trainer=trainer)

    context = {
        'trainer': trainer,
        'schedules': schedules,
    }
    return render(request, 'courses/trainer_schedule.html', context)

from django.http import JsonResponse

class FilterBy(APIView):
    def post(self, request):
        fregion = request.POST.get('fregion')
        fdate = request.POST.get('fdate')
        courseschedules = CourseSchedule.objects.filter(region=fregion, start_date=fdate)
        
        results = list(courseschedules.values(
            'region', 'start_date','end_date','schedule_start_time','schedule_end_time',  # CourseSchedule fields
            'trainer__trainer_name'  # ForeignKey field for trainer name
        ))
        
        return JsonResponse({'data': results})
class RemoveTrainer(APIView):
    def post(self, request):
        id = request.POST.get('id')
        AddTrainers.objects.filter(trainer_id = id).delete()
        return JsonResponse({"status":"pass"})
def payment_page(request, id):
    course = Course.objects.get(course_id = id)
    domains = Category.objects.all()
    user_id = request.session['customer_id']
    company_data = CompanyProfile.objects.filter(user_id = user_id)
    return render(request, 'courses/paymentpage.html',{'currentEmail':request.session['customer_email'],'course':course,"currentUser":request.session['user_name'],'currentUserId':request.session['customer_id'],'company_data':company_data,})
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from .models import Customer, Course, Payment  # Assuming these are your models
from django.conf import settings

from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.views import APIView
from django.conf import settings
from .models import Customer, Course, Payment

class StartPayment(APIView):
    def post(self, request):
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        transaction_id = request.POST.get('transaction_id')
        payment_img = request.FILES.get('payment_img')
        total_price = request.POST.get('total_price')
        user = Customer.objects.get(customer_id=user_id)
        course = Course.objects.get(course_id=course_id)
        if Payment.objects.filter(transaction_id = transaction_id).exists():
            return JsonResponse({"status":"transaction_id_exists","message":"This Transaction already Exists!"})
        payment = Payment()
        payment.user = user
        payment.course = course
        payment.amount = total_price
        payment.transaction_id = transaction_id
        payment.payment_proof = payment_img
        payment.save()
        user_email = user.email  
        course_name = course.title    
        subject = "Payment Confirmation"
        message = f"Dear {user.username},\n\nThank you for your payment for the course '{course_name}'.\nTransaction ID: {transaction_id}\n\nBest regards,\nYour Team"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],                 
            fail_silently=False,
        )
        messages.success(request, f'New payment uploaded by {user.username} for the course {course_name}.')

        return JsonResponse({"status": "pass"})


def add_to_cart(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        quantity = request.POST.get('quantity')
        customer_id = request.POST.get('customer_id')

        try:
            course = Course.objects.get(course_id=course_id)

            # Get the customer associated with the customer_id
            customer = get_object_or_404(Customer, customer_id=customer_id)

            # Create a cart entry
            Cart.objects.create(
                cid=customer,  # Assign the customer instance here
                course=course,
                quantity=quantity
            )
            return JsonResponse({'status': 'success'})
        except Course.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Medicine not found'})
        except Customer.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Customer not found'})
    
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'})