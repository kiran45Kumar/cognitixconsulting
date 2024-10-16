from django.shortcuts import render
from rest_framework.views import APIView
from customer.models import Customer
from .models import Trainer, Category
from adminuse.models import AddTrainers
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import Course,Enrollment
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
class CreateCourses(APIView):
    def post(self, request):
        title= request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        gst = request.POST.get('gst')
        total_price = request.POST.get('total_price')
        skillsgained = request.POST.get('skillsgained')
        img = request.FILES.get('img')
        category_id = request.POST.get('category')
        trainer = request.POST.get('trainer')
        started_at = request.POST.get('started_at')
        ended_at = request.POST.get('ended_at')
        cat = Category.objects.get(id = category_id)
        train = AddTrainers.objects.get(trainer_id = trainer)
        course = Course()
        course.title = title
        course.description = description
        course.course_gst = gst
        course.course_img = img
        course.total_price = total_price
        course.skillsgain = skillsgained
        course.price = price
        course.category = cat
        course.trainer = train
        course.started_at = started_at
        course.ended_at = ended_at
        course.save()
        return JsonResponse({"status":"pass"})
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
            temail = request.POST.get('temail')
            texperience = request.POST.get('texperience')
            tphone = request.POST.get('tphone')
            taddress = request.POST.get('taddress')
            timg = request.FILES.get('timg')
            addtrainer = AddTrainers()
            addtrainer.trainer_name = tname
            addtrainer.trainer_description = tdesc
            addtrainer.trainer_bio = tbio
            addtrainer.trainer_expertise = texpertise
            addtrainer.trainer_experience = texperience
            addtrainer.trainer_email = temail
            addtrainer.trainer_phone = tphone
            addtrainer.trainer_address = taddress
            addtrainer.trainer_photo = timg
            addtrainer.save()
            return JsonResponse({"status":"pass"})
class ViewCourses(TemplateView):
    template_name = 'courses/view_courses.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.all()
        context['courses'] = courses
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