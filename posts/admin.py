from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from .models import Post, Topic, PostComment


# Register your models here.
class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 0
    ordering = ('-created_at',)
    fields = ('author', 'content', 'created_at', 'like_count')
    readonly_fields = ('author', 'created_at', 'like_count')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'topic', 'like_count')
    list_filter = ('created_at', 'topic')
    search_fields = ('author', 'title', 'content')
    fields = ('author', 'topic', 'title', 'content', 'created_at', 'like_count')
    readonly_fields = ('author', 'created_at', 'like_count')
    list_select_related = ('author', 'topic')
    inlines = [PostCommentInline]


class TopicAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('order',)
    sortable = 'order'


admin.site.register(Post, PostAdmin)
admin.site.register(Topic, TopicAdmin)
