from django.core.management.base import BaseCommand
from api.models import Student
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Moves non ETU mails to the other mail field from mail_etu to mail_other'

    def handle(self, *args, **options):
        students = Student.objects.all()
        for student in tqdm(students, desc="Processing students"):
            if student.mail_etu is not None and not student.mail_etu.endswith("@etu.edu.tr"):
                student.mail_other = student.mail_etu
                student.mail_etu = None
                student.save()
        print("All students updated")
