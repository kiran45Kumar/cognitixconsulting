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
    