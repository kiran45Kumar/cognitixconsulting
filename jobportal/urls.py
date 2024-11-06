from django.urls import path
from .views import form_job,CreateJobs,ViewJobs,jobs,post_a_job,PostaJob,ViewJob,job_by_id,apply_job,CompanyDashboard
from . import views
urlpatterns = [
    path('post_job/',form_job, name='post_job'),
    path('create_job/',CreateJobs.as_view(), name='create_job'),
    path('post-job/',ViewJobs.as_view(),name='view_companies'),
    path('jobs/',jobs,name='jobs'),
    path('post_a_job/',post_a_job,name='post_a_job'),
    path('new_job/',PostaJob.as_view(),name='post_a_job'),
    path('all_jobs/',views.ViewJob.as_view(),name='all_jobs'),
    path('job/<int:id>/',job_by_id,name='all_jobs'),
    path('apply_job/<int:id>',apply_job,name='all_jobs'),
    path('company_dashboard/',CompanyDashboard.as_view(),name='company_dashboard'),
    path('company_jobs/<int:id>', views.company_jobs, name='company_jobs'),
    path("job_update/", views.JobUpdate.as_view(), name="job_update"),
    path("job_delete/",views.DeleteJobs.as_view(), name='delete_jobs'),
    path('remove_company/',views.RemoveAccount.as_view(), name="remove_account"),
    path('company_update/<int:id>/',views.view_company_form, name='company_update'),
    path('company_update/', views.UpdateCompany.as_view(), name='company_update_view'),
    path("company_delete/", views.CompanyDelete.as_view(), name='company_delete')
]