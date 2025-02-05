from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Student, Profile, Lesson, LessonSection, LessonSectionStudent, LessonSectionClassroom


class Command(BaseCommand):
    help = 'Gets the total lesson count of every student which take a particular lesson at given time'

    def handle(self, *args, **options):
        lesson_code = "MAK 316L"
        lesson_section_number_1 = 1
        lesson_section_number_2 = 2
        lesson_section_1 = LessonSection.objects.get(lesson_code=Lesson.objects.get(lesson_code=lesson_code), lesson_section_number=lesson_section_number_1)
        lesson_section_2 = LessonSection.objects.get(lesson_code=Lesson.objects.get(lesson_code=lesson_code), lesson_section_number=lesson_section_number_2)
        students_for_1 = LessonSectionStudent.objects.filter(lesson_section=lesson_section_1)
        students_for_2 = LessonSectionStudent.objects.filter(lesson_section=lesson_section_2)
        busy_students_count_at_times = [0] * 98
        for student in students_for_1:
            student_lessons = LessonSectionStudent.objects.filter(student=student.student)
            busy_times = set()
            for student_lesson in student_lessons:
                lesson_section_classrooms = LessonSectionClassroom.objects.filter(lesson_section=student_lesson.lesson_section)
                for lesson_section_classroom in lesson_section_classrooms:
                    busy_times.add(lesson_section_classroom.time)
            for busy_time in busy_times:
                busy_students_count_at_times[busy_time] += 1
        for student in students_for_2:
            student_lessons = LessonSectionStudent.objects.filter(student=student.student)
            busy_times = set()
            for student_lesson in student_lessons:
                lesson_section_classrooms = LessonSectionClassroom.objects.filter(lesson_section=student_lesson.lesson_section)
                for lesson_section_classroom in lesson_section_classrooms:
                    busy_times.add(lesson_section_classroom.time)
            for busy_time in busy_times:
                busy_students_count_at_times[busy_time] += 1
        for i in range(0, 98, 7):
            self.stdout.write(self.style.SUCCESS('\t'.join(f'{busy_students_count_at_times[j]}' for j in range(i, min(i + 7, 98)))))
            self.stdout.write('\n')
