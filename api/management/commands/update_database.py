import json
import locale
import os
import sqlite3
from random import random

from django.core.management import BaseCommand, call_command

from api.management.commands import create_student_profiles

DATABASE_NAME = 'db.sqlite3'
REQUEST_OUTPUT_DIR = 'request_output'
CLASSROOMS_FOLDER_PATH = os.path.join(REQUEST_OUTPUT_DIR, 'classrooms')
LESSONS_FOLDER_PATH = os.path.join(REQUEST_OUTPUT_DIR, 'lessons')
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')


class Command(BaseCommand):
    help = 'Updates the database with the latest data. Just put the new request_output folder in the root directory.'

    def handle(self, *args, **options):
        update_database()


def random_color():
    return f'#{int(random() * 0xffffff):06x}'


def update_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Remove old data
    cursor.execute('DELETE FROM lesson_section_classroom')
    cursor.execute('DELETE FROM lesson_section_student')
    cursor.execute('DELETE FROM lesson_section_teacher')
    cursor.execute('DELETE FROM time_empty_classroom')
    cursor.execute('DELETE FROM lesson_section')
    cursor.execute('DELETE FROM lesson')
    cursor.execute('DELETE FROM classroom')
    cursor.execute('DELETE FROM teacher')

    # Reset primary keys
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "lesson_section_classroom"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "lesson_section_student"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "lesson_section_teacher"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "time_empty_classroom"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "lesson_section"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "lesson"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "classroom"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "teacher"')

    # Get all student IDs before inserting new data
    cursor.execute('SELECT id FROM student')
    all_student_ids = {row[0] for row in cursor.fetchall()}

    # Insert or update new data
    lesson_files = os.listdir(LESSONS_FOLDER_PATH)

    print('Processing lesson files...')
    for lesson_file in lesson_files:
        with open(os.path.join(LESSONS_FOLDER_PATH, lesson_file), 'r') as file:
            lesson = json.load(file)
            lesson_file_parts = lesson_file.split(' ')
            lesson_code = lesson_file_parts[0] + ' ' + lesson_file_parts[1]
            lesson_name = ' '.join(lesson_file_parts[2:])[:-5]

            # Check if lesson exists
            cursor.execute('SELECT color FROM lesson WHERE lesson_code = ?', (lesson_code,))
            result = cursor.fetchone()
            if result:
                lesson_color = result[0]
            else:
                lesson_color = random_color()
            cursor.execute('INSERT INTO lesson (lesson_code, name, color) VALUES (?, ?, ?)',
                           (lesson_code, lesson_name, lesson_color))

            for section in lesson:
                cursor.execute('INSERT INTO lesson_section (lesson_section_number, lesson_code, color) VALUES (?, ?, ?)',
                               (section['SubeNo'], lesson_code, random_color()))
                current_lesson_section_id = cursor.lastrowid
                for student in section['Ogrenci']:
                    student['Ad'] = student['Ad'].title()
                    student['Soyad'] = student['Soyad'].title()

                    # Check if student exists
                    cursor.execute('SELECT color, mail_etu FROM student WHERE id = ?', (student['OgrenciNo'],))
                    result = cursor.fetchone()
                    if result:
                        student_color, student_mail = result
                        if "@etu.edu.tr" in student['Mail']:
                            student_mail = student['Mail']
                    else:
                        student_color = random_color()
                        student_mail = student['Mail']
                    cursor.execute('INSERT OR REPLACE INTO student (id, name, surname, department, mail, year, color) '
                                   'VALUES (?, ?, ?, ?, ?, ?, ?)',
                                   (student['OgrenciNo'], student['Ad'], student['Soyad'], student['ProgramAdi'],
                                    student_mail, student['Sinif'], student_color))
                    cursor.execute('INSERT INTO lesson_section_student (lesson_section_id, student_id) VALUES (?, ?)',
                                   (current_lesson_section_id, student['OgrenciNo']))
                    all_student_ids.discard(student['OgrenciNo'])

                section['OgretimUyesi'] = section['OgretimUyesi'].title()
                cursor.execute('INSERT OR IGNORE INTO teacher (name) VALUES (?)',
                               (section['OgretimUyesi'],))
                cursor.execute('INSERT INTO lesson_section_teacher (lesson_section_id, teacher_name) VALUES (?, ?)',
                               (current_lesson_section_id, section['OgretimUyesi']))

    classroom_files = os.listdir(CLASSROOMS_FOLDER_PATH)

    print('Processing classroom files...')
    for classroom_file in classroom_files:
        with open(os.path.join(CLASSROOMS_FOLDER_PATH, classroom_file), 'r') as file:
            classroom = json.load(file)
            classroom_name = classroom_file[:-5]
            cursor.execute('INSERT INTO classroom (name) VALUES (?)', (classroom_name,))
            hour_time = 0
            for section in classroom:
                for day in section['OgrenciDersProgram']:
                    day_time = day['Gun'] - 1
                    time = hour_time * 7 + day_time
                    if day['DersKodu'] != '-':
                        s = day['DersKodu'].split(' Şube')
                        lesson_code = s[0]
                        lesson_section_number = s[1]
                        cursor.execute(
                            'INSERT OR IGNORE INTO lesson_section (lesson_section_number, lesson_code, color) VALUES (?, ?, ?)',
                            (lesson_section_number, lesson_code, random_color()))
                        cursor.execute(
                            'SELECT id FROM lesson_section WHERE lesson_section_number = ? AND lesson_code = ?',
                            (lesson_section_number, lesson_code))
                        lesson_section_id = cursor.fetchone()[0]
                        cursor.execute(
                            'INSERT INTO lesson_section_classroom (lesson_section_id, classroom_name, time) VALUES (?, ?, ?)',
                            (lesson_section_id, classroom_name, time))
                hour_time += 1

    # Fill the time_empty_classroom table with classrooms that don't have lessons at time t
    for time in range(98):
        cursor.execute(
            '''INSERT INTO time_empty_classroom (classroom_name, time)
               SELECT DISTINCT classroom_name, ?
               FROM lesson_section_classroom
               WHERE classroom_name NOT IN (
                   SELECT classroom_name 
                   FROM lesson_section_classroom
                   WHERE time = ?
               )
               AND classroom_name NOT LIKE 'X%' ''', (time, time)
        )

    print('Processing remaining students...')
    for student_id in all_student_ids:
        cursor.execute('UPDATE student SET year = -1 WHERE id = ?', (student_id,))

    conn.commit()
    print('Successfully updated the database!')
    conn.close()

    call_command(create_student_profiles.Command())
