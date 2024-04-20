from django.urls import path
from . import views

urlpatterns = [
    path('get-posts/', views.GetPostsApiView.as_view(), name='posts'),
]