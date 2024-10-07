from django.db import models
from django.utils.timezone import now
from customer.models import Customer
from adminuse.models import AddTrainers

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    trainer = models.ForeignKey(AddTrainers, on_delete=models.CASCADE)
    started_at = models.DateField(default=now)
    ended_at = models.DateField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE) 
    enrolled_at = models.DateTimeField(auto_now_add=True)

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

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.course.title}"
