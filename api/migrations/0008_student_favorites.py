# Generated by Django 5.1.1 on 2025-02-07 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_student_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='favorites',
            field=models.ManyToManyField(blank=True, to='api.student'),
        ),
    ]
