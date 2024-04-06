from django.urls import path
from . import views

urlpatterns = [
    path('get-students/', views.GetStudentsApiView.as_view(), name='students'),
    path('get-student-info/', views.GetStudentInfoApiView.as_view(), name='student_info'),

    path('get-teachers/', views.GetTeachersApiView.as_view(), name='teachers'),
    path('get-teacher-info/', views.GetTeacherInfoApiView.as_view(), name='teacher_info'),
]
