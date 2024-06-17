from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Student, Profile


class Command(BaseCommand):
    help = 'Creates a profile for each student'

    def handle(self, *args, **options):
        students = Student.objects.all()
        student_count = students.count()
        completed = 0

        for student in students:
            completed += 1
            # Check if the student already has a profile
            if not Profile.objects.filter(student=student).exists():
                # Create a new user for each student
                user = User.objects.create_user(username=student.id, password='defaultpassword')

                # Create a new profile for each student
                Profile.objects.create(user=user, student=student)

                # Print the progress
                completed_percentage = (completed / student_count) * 100
                self.stdout.write(self.style.SUCCESS(f'{completed_percentage:.2f}% - Profile created for {student.name} {student.surname}'))

        self.stdout.write(self.style.SUCCESS('Successfully created profiles for all students'))
