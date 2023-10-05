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