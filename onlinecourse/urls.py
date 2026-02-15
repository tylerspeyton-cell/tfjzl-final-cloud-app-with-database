from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Path for the course details (Task 4)
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),

    # Path for exam submission (Task 5/6)
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    
    # Path for displaying exam results (Task 5/6)
    path('course/<int:course_id>/submission/<int:submission_id>/show_exam_result/', 
         views.show_exam_result, name='show_exam_result'),
]
