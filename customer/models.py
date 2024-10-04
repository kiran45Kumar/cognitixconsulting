from django.db import models

# Create your models here.
class Customer(models.Model):
    role_choices = [
        ("customer",'Customer'),
        ("admin","Admin")
    ]
    customer_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.IntegerField()
    password = models.CharField(max_length=200)
    confirm_password = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=role_choices,default='customer')

    def __str__(self) -> str:
        return self.username, self.customer_id
