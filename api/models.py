from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ForeignKey('Student', models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.student.name + " " + self.student.surname


class Student(models.Model):
    id = models.TextField(primary_key=True, blank=True, null=False)
    name = models.TextField(blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    mail = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.name + " - " + self.surname + " - " + self.department + " - " + str(self.year) + " - " + self.id


class Teacher(models.Model):
    name = models.TextField(primary_key=True, blank=True, null=False)

    class Meta:
        db_table = 'teacher'

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.TextField(primary_key=True, blank=True, null=False)

    class Meta:
        db_table = 'classroom'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    lesson_code = models.TextField(primary_key=True, blank=True, null=False)
    name = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'lesson'

    def __str__(self):
        return self.lesson_code + " - " + self.name


class LessonSection(models.Model):
    lesson_section_number = models.IntegerField(blank=True, null=True)
    lesson_code = models.ForeignKey(Lesson, models.CASCADE, db_column='lesson_code', blank=True, null=True)
    color = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'lesson_section'

    def __str__(self):
        return self.lesson_code.lesson_code + " - " + str(self.lesson_section_number)


class LessonSectionStudent(models.Model):
    lesson_section = models.ForeignKey(LessonSection, models.CASCADE, blank=True, null=True)
    student = models.ForeignKey('Student', models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'lesson_section_student'

    def __str__(self):
        return (self.lesson_section.lesson_code.lesson_code + " - " + str(self.lesson_section.lesson_section_number) +
                " - " + self.student.name)


class LessonSectionTeacher(models.Model):
    lesson_section = models.ForeignKey(LessonSection, models.CASCADE, blank=True, null=True)
    teacher_name = models.ForeignKey('Teacher', models.CASCADE, db_column='teacher_name', blank=True, null=True)

    class Meta:
        db_table = 'lesson_section_teacher'

    def __str__(self):
        return (self.lesson_section.lesson_code.lesson_code + " - " + str(self.lesson_section.lesson_section_number) +
                " - " + self.teacher_name.name)


class LessonSectionClassroom(models.Model):
    lesson_section = models.ForeignKey(LessonSection, models.CASCADE, blank=True, null=True)
    classroom_name = models.ForeignKey(Classroom, models.CASCADE, db_column='classroom_name', blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'lesson_section_classroom'

    def __str__(self):
        return (self.lesson_section.lesson_code.lesson_code + " - " + str(self.lesson_section.lesson_section_number) +
                " - " + self.classroom_name.name + " - " + str(self.time))


class TimeEmptyClassroom(models.Model):
    classroom_name = models.ForeignKey(Classroom, models.CASCADE, db_column='classroom_name', blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'time_empty_classroom'

    def __str__(self):
        return self.classroom_name.name + " - " + str(self.time)
