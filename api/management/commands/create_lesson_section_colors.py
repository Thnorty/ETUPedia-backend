from django.core.management import BaseCommand
import random
from api.models import LessonSection


class Command(BaseCommand):
    help = 'Creates random colors for each lesson'

    def handle(self, *args, **options):
        lesson_sections = LessonSection.objects.all()
        lesson_count = lesson_sections.count()
        completed = 0

        for lesson_section in lesson_sections:
            completed += 1
            lesson_section.color = get_random_color()
            lesson_section.save()

            completed_percentage = (completed / lesson_count) * 100
            self.stdout.write(self.style.SUCCESS(f'{completed_percentage:.2f}% - Color created for '
                                                 f'{lesson_section.lesson_code.name} - '
                                                 f'{lesson_section.lesson_section_number}'))

        self.stdout.write(self.style.SUCCESS('Successfully created colors for all lesson sections'))


def get_random_color():
    # generate a random color between 16777215 and 14680064
    return f'#{random.randint(14680064, 16777215):x}'
