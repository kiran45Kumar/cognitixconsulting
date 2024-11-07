# Generated by Django 5.1.1 on 2024-11-04 14:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddTrainers',
            fields=[
                ('trainer_id', models.AutoField(primary_key=True, serialize=False)),
                ('trainer_name', models.CharField(default='', max_length=200, unique=True)),
                ('trainer_desc', models.CharField(default='', max_length=200)),
                ('trainer_bio', models.CharField(max_length=500)),
                ('trainer_expertise', models.CharField(max_length=500)),
                ('trainer_experience', models.CharField(default='', max_length=500)),
                ('trainer_specialization', models.CharField(default='', max_length=200)),
                ('trainer_photo', models.ImageField(default='', upload_to='trainer_profiles/')),
                ('trainer_created', models.DateTimeField(auto_now_add=True)),
                ('trainer_updated', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
    ]
