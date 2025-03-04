from django.core.management import BaseCommand
from api.models import Lesson


class Command(BaseCommand):
    help = 'Finds common students in 2 lessons'

    def handle(self, *args, **options):
        lesson1_name = "BİL 331"
        lesson2_name = "BİL 395"
        lesson1_section = 1
        lesson2_section = 1

        lesson1 = Lesson.objects.get(lesson_code=lesson1_name).lessonsection_set.get(lesson_section_number=lesson1_section)
        lesson2 = Lesson.objects.get(lesson_code=lesson2_name).lessonsection_set.get(lesson_section_number=lesson2_section)

        students1 = lesson1.lessonsectionstudent_set.all()
        students2 = lesson2.lessonsectionstudent_set.all()

        # Get the student objects from each lesson section
        student_ids1 = set(student.student.id for student in students1)
        student_ids2 = set(student.student.id for student in students2)

        # Find common student IDs
        common_student_ids = student_ids1.intersection(student_ids2)

        # Get the actual student records
        common_students = [student for student in students1 if student.student.id in common_student_ids]

        common_students.sort(key=lambda student: (student.student.name, student.student.surname))

        self.stdout.write(self.style.SUCCESS(f'Common students in {lesson1_name} and {lesson2_name}:'))
        for student in common_students:
            self.stdout.write(self.style.SUCCESS(f'{student.student.name} {student.student.surname}'))
