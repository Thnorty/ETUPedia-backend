from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginApiView.as_view(), name='login'),

    path('get-teachers/', views.GetTeachersApiView.as_view(), name='teachers'),
    path('get-teacher-info/', views.GetTeacherInfoApiView.as_view(), name='teacher_info'),

    path('get-lessons/', views.GetLessonsApiView.as_view(), name='lessons'),
    path('get-lesson-info/', views.GetLessonInfoApiView.as_view(), name='lesson_info'),
    path('get-sections-of-lesson/', views.GetSectionsOfLessonApiView.as_view(), name='sections_of_lesson'),

    path('get-students/', views.GetStudentsApiView.as_view(), name='students'),
    path('get-student-info/', views.GetStudentInfoApiView.as_view(), name='student_info'),

    path('change-profile-color/', views.ChangeProfileColorApiView.as_view(), name='change_profile_color'),

    path('get-empty-classrooms/', views.GetEmptyClassroomsApiView.as_view(), name='empty_classrooms'),
]
