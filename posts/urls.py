from django.urls import path
from . import views

urlpatterns = [
    path('get-posts/', views.GetPostsApiView.as_view(), name='posts'),
    path('create-post/', views.CreatePostApiView.as_view(), name='create-post'),
    path('edit-post/', views.EditPostApiView.as_view(), name='edit-post'),
    path('delete-post/', views.DeletePostApiView.as_view(), name='delete-post'),
    path('create-comment/', views.CreateCommentApiView.as_view(), name='create-comment'),
    path('edit-comment/', views.EditCommentApiView.as_view(), name='edit-comment'),
    path('delete-comment/', views.DeleteCommentApiView.as_view(), name='delete-comment'),
    path('get-post-info/', views.GetPostInfoApiView.as_view(), name='post-info'),
    path('like-post/', views.LikePostApiView.as_view(), name='like-post'),
    path('like-comment/', views.LikeCommentApiView.as_view(), name='like-comment'),
    path('get-topics/', views.GetTopicsApiView.as_view(), name='topics'),
]
