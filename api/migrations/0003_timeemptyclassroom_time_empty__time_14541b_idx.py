# Generated by Django 5.1.1 on 2024-12-07 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_timeemptyclassroom'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='timeemptyclassroom',
            index=models.Index(fields=['time'], name='time_empty__time_14541b_idx'),
        ),
    ]
