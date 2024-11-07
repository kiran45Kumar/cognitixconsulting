from django.db import models
from customer.models import Customer
from datetime import time
from adminuse.models import Subscription

# Create your models here.
class CompanyProfile(models.Model):
    company_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_tagline = models.CharField(max_length=200,default="")
    company_logo = models.ImageField(upload_to="company_logos/", default="")
    company_location = models.CharField(max_length=200)
    company_desc = models.TextField()
    estblished = models.CharField(max_length=200)
    company_email = models.EmailField(max_length=200, unique=True)
    company_linkedin = models.URLField(max_length=500)
    company_instagram = models.URLField(max_length=500)
    company_facebook = models.URLField(max_length=500)
    company_address = models.CharField(max_length=500,default="")
    company_state = models.CharField(max_length=100,default="")
    company_city = models.CharField(max_length=500,default="")
    company_pincode = models.IntegerField(default=560078)
    company_profile_created_at = models.DateTimeField(auto_now_add=True)
    company_profile_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.company_name}, {self.company_location}'

from django.db import models
from django.contrib.auth.models import User

class PostJob(models.Model):
    EMPLOYMENT_TYPES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
        ('IN', 'Internship'),
    ]
    INDUSTRIES = (
        ('Tech', 'Technology'),
        ('Health', 'Healthcare'),
        ('Finance', 'Finance and Insurance'),
        ('Retail', 'Retail'),
        ('Manufacturing', 'Manufacturing'),
        ('Construction', 'Construction'),
        ('Education', 'Education'),
        ('Transport', 'Transportation and Logistics'),
        ('Hospitality', 'Hospitality and Tourism'),
        ('Govt', 'Government'),
        ('Telecom', 'Telecommunications'),
        ('Energy', 'Energy and Utilities'),
        ('Media', 'Media and Entertainment'),
        ('Pharma', 'Pharmaceuticals'),
        ('NonProfit', 'Non-profit Organizations'),
        ('Agriculture', 'Agriculture'),
        ('Consulting', 'Consulting'),
        ('Legal', 'Legal Services'),
        ('Fashion', 'Fashion'),
        ('Automotive', 'Automotive'),
    )
    # Basic job info
    job_id  = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="Application Developer")
    company_posted_by = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE,default="")  # The user posting the job
    location = models.CharField(max_length=100,default="")
    job_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPES, default='FT')
    reports_to = models.CharField(max_length=100, blank=True, null=True,default="")
    
    # Job description fields
    summary = models.TextField()  # General overview of the job
    responsibilities = models.TextField()  # Key responsibilities of the role
    qualifications = models.TextField()  # Mandatory qualifications
    preferred_qualifications = models.TextField(blank=True, null=True)  # Optional qualifications
    skills = models.TextField()  # Required skills for the job
    benefits = models.TextField(blank=True, null=True)  # Job benefits (optional)
    
    # Additional details
    salary = models. CharField(max_length=200,default="")  # Optional salary
    timings = models.CharField(max_length=200,default="")  # Optional salary
    posted_on = models.DateTimeField(auto_now_add=True)  # Auto-set when job is posted
    last_date_to_apply = models.DateField(blank=True, null=True)  # Application deadline
    category = models.CharField(max_length=100, default="")  # Store category name as a string

    # Industry type
    industry = models.CharField(max_length=100, choices=INDUSTRIES, default='Tech')
    
    def __str__(self):
        return f"{self.title} at {self.company_posted_by.company_name}"
from django.db import models

class JobApplications(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    job = models.ForeignKey(PostJob, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('applied', 'Applied'),
            ('interview', 'Interview'),
            ('rejected', 'Rejected'),
            ('accepted', 'Accepted')
        ],
        default='applied'
    )
    applicant_name = models.CharField(max_length=200)
    education = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    previous_companies = models.TextField(null=True, blank=True)
    previous_experience = models.TextField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    cover_letter = models.FileField(upload_to='cover_letters/', null=True, blank=True)
    salary_expectation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_feedback = models.TextField(null=True, blank=True)
    application_source = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.applicant_name} applied for {self.job}"
    
class PaymentforCompanies(models.Model):
    payment_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    plan = models.ForeignKey(Subscription, on_delete=models.CASCADE)
