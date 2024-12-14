from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from backend import settings
urlpatterns = [
    re_path(r'^favicon\.ico$', serve, {'path': 'favicon.ico', 'document_root': settings.STATIC_URL}),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('posts/', include('posts.urls')),
]
