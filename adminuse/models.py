from django.db import models
from django.utils.timezone import now
from customer.models import Customer

# Create your models here.
class AddTrainers(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    trainer_name = models.CharField(max_length=200,unique=True,default="")
    user_id = models.ForeignKey(Customer, default="", on_delete=models.CASCADE)
    trainer_desc = models.CharField(max_length=200, default='')
    trainer_bio = models.CharField(max_length=500)
    trainer_expertise = models.CharField(max_length=500)
    trainer_experience = models.CharField(max_length=500,default="")
    trainer_specialization = models.CharField(max_length=200, default='')
    trainer_photo = models.ImageField(upload_to="trainer_profiles/",default='')
    trainer_created = models.DateTimeField(auto_now_add=True)
    trainer_updated = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f'{self.trainer_name}'
from django.db import models

class Subscription(models.Model):
    BASIC = 'Basic'
    STANDARD = 'Standard'
    PREMIUM = 'Premium'

    SUBSCRIPTION_CHOICES = [
        (BASIC, 'Basic'),
        (STANDARD, 'Standard'),
        (PREMIUM, 'Premium'),
    ]
    DURATION_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    subscription_id = models.AutoField(primary_key=True)
    subscription_name = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, unique=True)
    subscription_features = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default='monthly')
    is_active = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    max_users = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.subscription_name} - ${self.amount}"

