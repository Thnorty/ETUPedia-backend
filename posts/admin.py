from django.contrib import admin


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'content')
    ordering = ('title',)
