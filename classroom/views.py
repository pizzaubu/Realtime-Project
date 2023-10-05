from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, TeacherRegistrationForm
from classroom.models import *

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_success_page')  # เปลี่ยนไปยัง URL ของหน้าที่ต้องการหลังจากการลงทะเบียน
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/student_register.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_success_page')  # เปลี่ยนไปยัง URL ของหน้าที่ต้องการหลังจากการลงทะเบียน
    else:
        form = TeacherRegistrationForm()
    return render(request, 'registration/teacher_register.html', {'form': form})

def home(req):
    return render(req, 'classroom/home.html')

def student(req):
     return render(req, 'classroom/student.html')

def teacher(req):
     return render(req,'classroom/teacher.html')

def create_course(subject_name, teach_date, start_time, end_time):
    return Course.objects.create(
        subject_name=subject_name,
        teach_date=teach_date,
        start_time=start_time,
        end_time=end_time
    )

def add_student_to_course(student_id, course_id):
    student = Student.objects.get(pk=student_id)
    course = Course.objects.get(pk=course_id)
    return CourseStudent.objects.create(student=student, course=course)

def add_teacher_to_course(teacher_id, course_id):
    teacher = Teacher.objects.get(pk=teacher_id)
    course = Course.objects.get(pk=course_id)
    return CourseTeacher.objects.create(teacher=teacher, course=course)

def get_students_of_course(course_id):
    return [cs.student for cs in CourseStudent.objects.filter(course_id=course_id)]

def get_teachers_of_course(course_id):
    return [ct.teacher for ct in CourseTeacher.objects.filter(course_id=course_id)]

def remove_student_from_course(student_id, course_id):
    CourseStudent.objects.filter(student_id=student_id, course_id=course_id).delete()

def remove_teacher_from_course(teacher_id, course_id):
    CourseTeacher.objects.filter(teacher_id=teacher_id, course_id=course_id).delete()