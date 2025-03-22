from django.core.management import BaseCommand
from api.models import Lesson


class Command(BaseCommand):
    help = 'Get students for a lesson'

    def handle(self, *args, **options):
        lesson_name = "MAK 316L"

        lesson = Lesson.objects.get(lesson_code=lesson_name)
        lesson_sections = lesson.lessonsection_set.all()

        for lesson_section in lesson_sections:
            self.stdout.write(self.style.SUCCESS(f'{lesson_section}'))

            # Get all students enrolled in this section
            students = lesson_section.lessonsectionstudent_set.all()

            if students.exists():
                # Sort students alphabetically by name then surname
                sorted_students = sorted(students, key=lambda s: (s.student.name, s.student.surname))

                for i, student in enumerate(sorted_students, 1):
                    self.stdout.write(f"  {i}. {student.student.name} {student.student.surname}"
                                      f" {student.student.id} {student.student.mail_etu or student.student.mail_other}")
            else:
                self.stdout.write("  No students enrolled in this section")

            self.stdout.write("")  # Empty line between sections
