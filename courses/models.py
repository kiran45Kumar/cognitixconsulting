from django.db import models
from django.utils.timezone import now
from customer.models import Customer
from adminuse.models import AddTrainers


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    bio = models.TextField(blank=True, null=True)
    expertise = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True, null=True)
    def __str__(self):
        return f"{self.Customer.username} - {self.expertise}"
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    course_gst = models.IntegerField(default=18.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    course_img = models.ImageField(upload_to='course_images/', default="")
    course_video = models.FileField(upload_to="course_videos/", default="")
    course_sample_certificate = models.ImageField(upload_to="sample_certificates", default="")
    course_brochure = models.FileField(upload_to="brochures/", default="")
    trainers = models.ManyToManyField(AddTrainers)
    skillsgain = models.CharField(max_length=500, default="")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    completion_of_days = models.CharField(max_length=200, default="2days")
    completion_of_hrs = models.CharField(max_length=200, default="20hrs")
    start = models.DateField(default=now)
    end = models.DateField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_duration_days(self):
        return (self.ended_at - self.started_at).days
    def get_duration_hours(self):
        duration = self.ended_at - self.started_at  # This will give a timedelta object
        total_hours = duration.total_seconds() // 3600  # Convert total seconds to hours
        return total_hours

class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    access_granted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('customer', 'course')

    def __str__(self):
        return f"{self.customer.username} enrolled in {self.course.title}"


class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
from django.utils.timezone import now

from django.utils import timezone

class CourseSchedule(models.Model):
    trainer = models.ForeignKey(AddTrainers, default="", on_delete=models.CASCADE)
    region = models.CharField(max_length=200, default="")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    schedule_start_time = models.TimeField()  # Start time of the schedule
    schedule_end_time = models.TimeField()    # End time of the schedule
    notes = models.TextField(blank=True, null=True) #optional 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.trainer.name} ({self.start_date} - {self.end_date})"

    def get_duration_days(self):
        return (self.end_date - self.start_date).days


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.course.title}"


class Payment(models.Model):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    REJECTED = 'Rejected'
    
    PAYMENT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True,unique=True)
    payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)  # User uploads screenshot
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PENDING)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.course.title} by {self.user.username} - {self.status}"
