from django.urls import path
from . import views

urlpatterns = [
    path('hello-world/', views.HelloWorldApiView.as_view(), name='hello-world'),
    path('get-students/', views.GetStudentsApiView.as_view(), name='students'),
    path('get-student-info/', views.GetStudentInfoApiView.as_view(), name='student'),
]
