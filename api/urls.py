from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('id-of-not-found-student/', views.IDOfNotFoundStudentApiView.as_view(), name='id_of_not_found_student'),
    path('verify-email-of-not-found-student/', views.VerifyEmailOfNotFoundStudentApiView.as_view(), name='verify_email_of_not_found_student'),

    path('get-teachers/', views.GetTeachersApiView.as_view(), name='teachers'),
    path('get-teacher-info/', views.GetTeacherInfoApiView.as_view(), name='teacher_info'),

    path('get-lessons/', views.GetLessonsApiView.as_view(), name='lessons'),
    path('get-lesson-info/', views.GetLessonInfoApiView.as_view(), name='lesson_info'),
    path('get-sections-of-lesson/', views.GetSectionsOfLessonApiView.as_view(), name='sections_of_lesson'),

    path('get-students/', views.GetStudentsApiView.as_view(), name='students'),
    path('get-student-info/', views.GetStudentInfoApiView.as_view(), name='student_info'),
    path('favorite-student/', views.FavoriteStudentApiView.as_view(), name='favorite_student'),
    path('remove-favorite-student/', views.RemoveFavoriteStudentApiView.as_view(), name='remove_favorite_student'),

    path('change-profile-color/', views.ChangeProfileColorApiView.as_view(), name='change_profile_color'),

    path('get-empty-classrooms/', views.GetEmptyClassroomsApiView.as_view(), name='empty_classrooms'),
]
