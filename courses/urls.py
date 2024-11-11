from django.urls import path    
from .views import trainer, CreateTrainer,category,CreateCategory,ViewCategory,AddTrainer,CreateCourses,UpdateCourses,ViewCourses,DeleteCourse,Enroll_user,CoursesEnrollForUser,enrolledUsers,ViewTrainers,viewCourseById,ViewAllTrainer
from . import views
from .views import trainer_schedule
urlpatterns = [
    path('trainer/',trainer, name='trainer'),
    path('create_trainer/',CreateTrainer.as_view(), name='create_trainer'),
    path('categories/',category, name='add_category'),
    path('create_category/',CreateCategory.as_view(), name='create_category'),
    path('add_courses/',ViewCategory.as_view(), name='view_category'),
    path('add_trainer/',AddTrainer.as_view(), name='add_trainer'),
    path('create_courses/',CreateCourses.as_view(), name='create_courses'),
    path('update_courses/',UpdateCourses.as_view(), name='update_courses'),
    path('view-courses/',ViewCourses.as_view(), name='view_courses'),
    path('delete_courses/',DeleteCourse.as_view(), name='delete_courses'),
    path('enroll_user/',Enroll_user.as_view(), name='Enroll_user'),
    path('course_enrolled/',CoursesEnrollForUser.as_view(), name='course_enrolled'),
    path('enrolled_users/',enrolledUsers, name='enrolled_users'),
    path('view_trainer/',ViewTrainers.as_view(), name='view_trainer'),
    path('course/<int:id>',viewCourseById, name='all_courses'),
    path('view-trainers',ViewAllTrainer.as_view(), name='view-trainers'),
    path('delete_category/',views.DeleteCategory.as_view(),name='delete_category'),
    path('create_schedule/',views.CreateSchedule.as_view(),name='create_schedule'),
    path('schedule/<int:id>',views.schedule,name='schedule'),
    path('view_schedules',views.VieWScheduleAdmin.as_view(), name="view_schedules"),
    path('remove_schedule/',views.RemoveScheduleAdmin.as_view(), name="remove_schedule"),
    path('download_brochure/<int:course_id>/', views.download_brochure, name='download_brochure'),
    path('trainer/<int:trainer_id>/schedule/', trainer_schedule, name='trainer_schedule'),
    path('filter_by/',views.FilterBy.as_view(), name='filter_by'),
    path("remove_trainer/",views.RemoveTrainer.as_view(),name='remove_trainer' ),
    path('payment_page/<int:id>',views.payment_page, name='payment_page'),
    path('start_payment/',views.StartPayment.as_view(), name='start_payment'),
    path('cart_add/', views.add_to_cart, name='cart_add'),
    path('cart_page/<int:cid>', views.cart_page, name='cart_page'),
    path('enroll_page/<int:id>',views.enroll_page, name='enroll_page')
]