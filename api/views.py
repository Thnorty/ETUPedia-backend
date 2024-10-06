import requests
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.logging_utils import log
from api.models import Student, Teacher, Classroom, Lesson, LessonSection, LessonSectionStudent, \
    LessonSectionClassroom, LessonSectionTeacher, Profile


# Create your views here.
class LoginApiView(APIView):
    @staticmethod
    def post(request):
        email = request.data.get('email')
        oturum_no = request.data.get('oturumNo')

        if not email or not oturum_no:
            log(level='error', message='Missing email or oturumNo', request=request)
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        test_url = "https://program.etu.edu.tr/DersProgrami/api/dersprogramplan/bosderslik?dil=tr&oturumNo=" + oturum_no

        response = requests.get(test_url)
        if response.status_code != 200:
            log(level='error', message='Invalid email or oturumNo', request=request)
            return JsonResponse({'error': 'Wrong email or password'}, status=400)

        try:
            if '@' not in email:
                email = email + '@etu.edu.tr'
            student = Student.objects.get(mail=email)
            profile = Profile.objects.get(student=student)
        except Student.DoesNotExist:
            log(level='error', message='Student not found', request=request)
            return JsonResponse({'error': 'Student not found'}, status=400)
        except Profile.DoesNotExist:
            log(level='error', message='Profile not found', request=request)
            return JsonResponse({'error': 'Profile not found'}, status=400)

        token, created = Token.objects.get_or_create(user=profile.user)
        return JsonResponse({'student_id': student.id, 'token': token.key}, status=200)


class GetStudentsApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        students = Student.objects.all().order_by('name', 'surname')
        response = []
        for student in students:
            response.append({
                'id': student.id,
                'name': student.name,
                'surname': student.surname,
                'department': student.department,
                'mail': student.mail,
                'year': student.year,
                'color': student.color
            })
        return JsonResponse(response, safe=False)


class GetStudentInfoApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        student_id = request.data['student_id']
        student = Student.objects.get(id=student_id)
        student_lesson_sections = LessonSectionStudent.objects.filter(student=student)
        lesson_sections = []
        for section in student_lesson_sections:
            lesson_section_classrooms = LessonSectionClassroom.objects.filter(lesson_section=section.lesson_section)
            classrooms_and_times = [
                {'classroom': lsc.classroom_name.name, 'time': lsc.time} for lsc in lesson_section_classrooms
            ]
            lesson_sections.append({
                'lesson_code': section.lesson_section.lesson_code.lesson_code,
                'lesson_name': section.lesson_section.lesson_code.name,
                'lesson_section_number': section.lesson_section.lesson_section_number,
                'color': section.lesson_section.color,
                'classrooms_and_times': classrooms_and_times
            })
        response = {
            'id': student.id,
            'name': student.name,
            'surname': student.surname,
            'department': student.department,
            'mail': student.mail,
            'year': student.year,
            'color': student.color,
            'lesson_sections': lesson_sections
        }
        return JsonResponse(response, safe=False)


class ChangeProfileColorApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        student = request.user.profile.student
        color = request.data['color']
        student.color = color
        student.save()
        return JsonResponse({'message': 'Color changed successfully'}, status=200)


class GetTeachersApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        teachers = Teacher.objects.all().order_by('name')
        response = []
        for teacher in teachers:
            response.append({
                'name': teacher.name
            })
        return JsonResponse(response, safe=False)


class GetTeacherInfoApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        teacher_name = request.data['teacher_name']
        teacher = Teacher.objects.get(name=teacher_name)
        teacher_lesson_sections = LessonSectionTeacher.objects.filter(teacher_name=teacher)
        lesson_sections = []
        for section in teacher_lesson_sections:
            lesson_section_classrooms = LessonSectionClassroom.objects.filter(lesson_section=section.lesson_section)
            classrooms_and_times = [
                {'classroom': lsc.classroom_name.name, 'time': lsc.time} for lsc in lesson_section_classrooms
            ]
            lesson_sections.append({
                'lesson_code': section.lesson_section.lesson_code.lesson_code,
                'lesson_name': section.lesson_section.lesson_code.name,
                'lesson_section_number': section.lesson_section.lesson_section_number,
                'color': section.lesson_section.color,
                'classrooms_and_times': classrooms_and_times
            })
        response = {
            'name': teacher.name,
            'lesson_sections': lesson_sections
        }
        return JsonResponse(response, safe=False)


class GetClassroomsApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        classrooms = Classroom.objects.all()
        response = []
        for classroom in classrooms:
            response.append({
                'name': classroom.name
            })
        return JsonResponse(response, safe=False)


class GetLessonsApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        lessons = Lesson.objects.all()
        response = []
        for lesson in lessons:
            response.append({
                'lesson_code': lesson.lesson_code,
                'name': lesson.name
            })
        return JsonResponse(response, safe=False)


class GetLessonInfoApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        lesson_code = request.data['lesson_code']
        lesson = Lesson.objects.get(lesson_code=lesson_code)
        lesson_sections = LessonSection.objects.filter(lesson_code=lesson)
        lesson_section_count = len(lesson_sections)
        lesson_section_students = (LessonSectionStudent.objects.filter(lesson_section__in=lesson_sections)
                                   .order_by('student__name', 'student__surname'))
        students = [{'id': lss.student.id, 'name': lss.student.name, 'surname': lss.student.surname, 'color': lss.student.color} for lss in lesson_section_students]
        lesson_name = lesson.name
        student_count = len(lesson_section_students)
        response = {
            'lesson_code': lesson_code,
            'lesson_name': lesson_name,
            'lesson_section_count': lesson_section_count,
            'student_count': student_count,
            'students': students
        }
        return JsonResponse(response, safe=False)


class GetSectionsOfLessonApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        lesson_code = request.data['lesson_code']
        lesson = Lesson.objects.get(lesson_code=lesson_code)
        lesson_sections = LessonSection.objects.filter(lesson_code=lesson)
        response = []
        for lesson_section in lesson_sections:
            lesson_section_classrooms = LessonSectionClassroom.objects.filter(lesson_section=lesson_section)
            classrooms_and_times = [
                {'classroom': lsc.classroom_name.name, 'time': lsc.time} for lsc in lesson_section_classrooms
            ]
            response.append({
                'lesson_code': lesson_section.lesson_code.lesson_code,
                'lesson_name': lesson_section.lesson_code.name,
                'lesson_section_teacher': lesson_section.lessonsectionteacher_set.first().teacher_name.name,
                'lesson_section_number': lesson_section.lesson_section_number,
                'color': lesson_section.color,
                'classrooms_and_times': classrooms_and_times
            })
        return JsonResponse(response, safe=False)


class GetLessonSectionsApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        lesson_sections = LessonSection.objects.all()
        response = []
        for lesson_section in lesson_sections:
            response.append({
                'lesson_section_number': lesson_section.lesson_section_number,
                'lesson_code': lesson_section.lesson_code.lesson_code,
                'color': lesson_section.color
            })
        return JsonResponse(response, safe=False)
