from django.urls import path
from . import views

urlpatterns = [
    path('get-posts/', views.GetPostsApiView.as_view(), name='posts'),
    path('create-post/', views.CreatePostApiView.as_view(), name='create-post'),
]