from typing import Any
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import PostJob, CompanyProfile
from customer.models import Customer
from django.views.generic.base import TemplateView
from jobportal.models import JobApplications
# Create your views here.
def form_job(request):
    customer_id = request.session['customer_id']
    company_data = CompanyProfile.objects.filter(user_id =  customer_id)
    return render(request, 'jobportal/job_form.html',{'currentUserId':customer_id,"company_data":company_data})
class CreateJobs(APIView):
    def post(self, request):
        customer_id = request.POST.get('currentUserId')
        cname = request.POST.get('cname')
        company_logo = request.FILES.get('company_logo')
        cdesc = request.POST.get('cdesc')
        cloc = request.POST.get('cloc')
        cest = request.POST.get('cest')
        cemail = request.POST.get('cemail')
        ctagline = request.POST.get('ctagline')
        clinkedin = request.POST.get('clinkedin')
        cinstagram = request.POST.get('cinstagram')
        cfacebook = request.POST.get('cfacebook')
        caddress = request.POST.get('caddress')
        cstate = request.POST.get('cstate')
        ccity = request.POST.get('ccity')
        cpincode = request.POST.get('cpincode')
        customer = Customer.objects.get(customer_id = customer_id)
        jobs = CompanyProfile()
        if CompanyProfile.objects.filter(company_email = cemail).exists():
            return JsonResponse({"status":"fail","message":"Email Already Exists"})
        jobs.user_id = customer
        jobs.company_name = cname
        jobs.company_logo = company_logo
        jobs.company_desc = cdesc
        jobs.company_location = cloc
        jobs.estblished = cest
        jobs.company_tagline = ctagline
        jobs.company_email = cemail
        jobs.company_linkedin = clinkedin
        jobs.company_instagram = cinstagram
        jobs.company_facebook = cfacebook
        jobs.company_address = caddress
        jobs.company_state = cstate
        jobs.company_city = ccity
        jobs.company_pincode = cpincode
        jobs.save()
        return JsonResponse({"status":"pass"})
class ViewJobs(TemplateView):
    template_name = 'jobportal/jobview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_data = CompanyProfile.objects.filter(user_id =  self.request.session['customer_id'])
        context['company_data'] = company_data
        context['currentuser'] = self.request.session['user_name']
        return context
def jobs(request):
    return render(request, 'jobportal/jobs.html')
def post_a_job(request):
    return render(request, 'jobportal/postjob.html')
class ViewCompanies(TemplateView):
    template_name = 'jobportal/jobs.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_data = CompanyProfile.objects.filter(user_id =  self.request.session['customer_id'])
        currentUser = Customer.objects.get(customer_id = self.request.session['customer_id'])
        context['company_data'] = company_data
        return context
class PostaJob(APIView):
    def post(self, request):
        job_title = request.POST.get('job_title')
        company_posted_id = request.POST.get('company_posted_by')
        summary = request.POST.get('summary')
        job_type = request.POST.get('job_type')
        location = request.POST.get('location')
        responsibilities = request.POST.get('responsibilities')
        reportsto = request.POST.get('reportsto')
        category = request.POST.get('category')
        industry = request.POST.get('industry')
        timings = request.POST.get('timings')
        qualifications = request.POST.get('qualifications')
        preferred_qualifications = request.POST.get('preferred_qualifications')
        skills = request.POST.get('skills')
        salary = request.POST.get('salary')
        benefits = request.POST.get('benefits')
        last_date_to_apply = request.POST.get('last_date_to_apply')
        company = CompanyProfile.objects.get(company_id = company_posted_id)

        post = PostJob()
        post.title = job_title
        post.summary = summary
        post.job_type = job_type
        post.location = location
        post.responsibilities = responsibilities
        post.timings = timings
        post.qualifications = qualifications
        post.preferred_qualifications = preferred_qualifications
        post.skills = skills
        post.salary = salary
        post.benefits = benefits
        post.reports_to = reportsto
        post.category = category
        post.industry = industry
        post.last_date_to_apply = last_date_to_apply
        post.company_posted_by = company
        post.save()
        request.session['job_id'] = post.job_id
        return JsonResponse({"status":"pass"})
    
class ViewJob(TemplateView):
    template_name = 'jobportal/viewjobs.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_jobs = PostJob.objects.all().order_by('-posted_on')
        job = PostJob()
        job_id = job.job_id
        context['alljobs'] = all_jobs
        context['job_id'] = self.request.session.get('job_id')
        return context
def job_by_id(request,id):
    job = PostJob.objects.get(job_id = id)
    return render(request, 'jobportal/applyjobs.html',{"job":job})
def apply_job(request, id):
    context = {}
    user = request.session['customer_id']
    customer = Customer.objects.filter(customer_id = user)
    job = PostJob.objects.get(job_id = id)
    context['customers'] = customer
    context['jobs'] = job
    return render(request, 'jobportal/apply_jobs.html',context=context)
class CompanyDashboard(TemplateView):
    template_name = 'jobportal/companydashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['customer_id']
        company_data = CompanyProfile.objects.filter(user_id = user_id)
        context['company_data'] = company_data
        return context
class JobView(TemplateView):
    template_name = 'jobportal/apply_jobs.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.session.get('customer_id')
        context['user_id'] = user
        return context
class ApplyToJob(APIView):
    def post(self, request):
        user_id = request.POST.get('user_id')
        job_id = request.POST.get('job_id')
        applicant_name = request.POST.get('applicant_name')
        education = request.POST.get('education')
        skills = request.POST.get('skills')
        previous_companies = request.POST.get('previous_companies')
        resume = request.FILES.get('resume')
        cover_letter = request.FILES.get('cover_letter')
        salary_expectation = request.POST.get('salary_expectation')
        user = Customer.objects.get(customer_id = user_id)
        job = PostJob.objects.get(job_id = job_id)
        application = JobApplications()
        application.applicant_name = applicant_name
        application.education = education
        application.skills = skills
        application.previous_companies = previous_companies
        application.resume = resume
        application.cover_letter = cover_letter
        application.salary_expectation = salary_expectation
        application.user = user
        application.job = job
        application.save()
        return JsonResponse({"status":"pass"})
