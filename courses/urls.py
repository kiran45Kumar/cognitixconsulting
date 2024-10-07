from django.urls import path    
from .views import trainer, CreateTrainer,category,CreateCategory,ViewCategory,AddTrainer
urlpatterns = [
    path('trainer/',trainer, name='trainer'),
    path('create_trainer/',CreateTrainer.as_view(), name='create_trainer'),
    path('categories/',category, name='add_category'),
    path('create_category/',CreateCategory.as_view(), name='create_category'),
    path('add_courses/',ViewCategory.as_view(), name='view_category'),
    path('add_trainer/',AddTrainer.as_view(), name='add_trainer'),
]