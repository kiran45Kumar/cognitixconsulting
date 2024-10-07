from django.db import models

# Create your models here.
class AddTrainers(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    trainer_name = models.CharField(max_length=200)
    trainer_description = models.CharField(max_length=500)
    trainer_bio = models.CharField(max_length=500)
    trainer_expertise = models.CharField(max_length=500)
    trainer_email = models.EmailField(max_length=80, unique=True)
    trainer_phone = models.IntegerField(default=9999999999)
    trainer_address = models.CharField(max_length=200, default='Street Name, City, State pincode')
    trainer_created = models.DateTimeField(auto_now_add=True)
    trainer_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.trainer_name} - {self.trainer_description}'
    