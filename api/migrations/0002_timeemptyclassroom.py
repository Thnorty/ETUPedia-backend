# Generated by Django 5.1.1 on 2024-12-04 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeEmptyClassroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(blank=True, null=True)),
                ('classroom_name', models.ForeignKey(blank=True, db_column='classroom_name', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.classroom')),
            ],
            options={
                'db_table': 'time_empty_classroom',
            },
        ),
    ]
