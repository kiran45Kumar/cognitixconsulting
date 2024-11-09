from django.urls import path
from .views import addTrainer,adminDashboard,trainerFunction
from . import views
urlpatterns = [
    path('trainer_view/', addTrainer, name="add_trainer"),
    path('admin_dashboard/', adminDashboard, name="admin_dashboard"),
    path('view_trainer/<int:id>', trainerFunction, name="trainer_view"),
    path('view_all_jobs/',views.view_all_jobs, name='view_all_jobs'), 
    path('view_all_companies/',views.view_all_companies, name='view_all_companies'), 
    path('view_all_customers/',views.view_all_customers,name='view_all_customers'),
    path('remove_job/',views.DeleteJobs.as_view(), name='remove_job'), 
    path('remove_company_admin/',views.DeleteCompany.as_view(), name='remove_company_admin'),   
    path('update_user_admin/',views.UpdateUser.as_view(), name='update_user_admin'),
    path('delete_user_admin/',views.DeleteUser.as_view(), name='delete_user_admin'),
    path('view_messages/',views.view_all_messages, name='view_messages'),
    path('update-status/',views.UpdateStatus.as_view(),name='update-status'),
    path('reject-payment/',views.RejectPayment.as_view(), name='reject-payment'),
    path('remove-payment/',views.RemovePayment.as_view(), name='remove-payment'),
    path('add-subscription/',views.AddSubscription.as_view(), name='add_subscription'),
    path('subscription/',views.subscription_html, name='subscription'),
    path('admin_dash/',views.adminDash, name='admin_dash')
]