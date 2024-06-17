from django.core.management import BaseCommand
import random
from api.models import Lesson


class Command(BaseCommand):
    help = 'Creates random colors for each lesson'

    def handle(self, *args, **options):
        lessons = Lesson.objects.all()
        lesson_count = lessons.count()
        completed = 0

        for lesson in lessons:
            completed += 1
            lesson.color = get_random_color()
            lesson.save()

            completed_percentage = (completed / lesson_count) * 100
            self.stdout.write(self.style.SUCCESS(f'{completed_percentage:.2f}% - Color created for {lesson.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully created colors for all lessons'))


def get_random_color():
    # generate a random color between 16777215 and 14680064
    return f'#{random.randint(14680064, 16777215):x}'
