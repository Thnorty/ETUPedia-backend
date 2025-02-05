from django.contrib import admin
from .models import Student, Teacher, Classroom, Lesson, LessonSection, LessonSectionStudent, LessonSectionTeacher, \
    LessonSectionClassroom


# Create inlines for the models
class LessonSectionInline(admin.TabularInline):
    model = LessonSection
    extra = 0


class LessonSectionStudentInline(admin.TabularInline):
    model = LessonSectionStudent
    extra = 0


class LessonSectionTeacherInline(admin.TabularInline):
    model = LessonSectionTeacher
    extra = 0


class LessonSectionClassroomInline(admin.TabularInline):
    model = LessonSectionClassroom
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    inlines = (LessonSectionStudentInline, )
    search_fields = ('id', 'name', 'surname', 'department', 'mail_etu', 'mail_other', 'year')
    ordering = ('name', 'department', 'year')


class TeacherAdmin(admin.ModelAdmin):
    inlines = (LessonSectionTeacherInline, )
    search_fields = ('name', )
    ordering = ('name', )


class ClassroomAdmin(admin.ModelAdmin):
    inlines = (LessonSectionClassroomInline, )
    search_fields = ('name', )
    ordering = ('name', )


class LessonAdmin(admin.ModelAdmin):
    inlines = (LessonSectionInline, )
    search_fields = ('lesson_code', 'name')
    ordering = ('lesson_code', 'name')


class LessonSectionAdmin(admin.ModelAdmin):
    inlines = (LessonSectionStudentInline, LessonSectionTeacherInline, LessonSectionClassroomInline)
    search_fields = ('lesson_code', 'lesson_section_number')
    ordering = ('lesson_code', 'lesson_section_number')


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonSection, LessonSectionAdmin)
