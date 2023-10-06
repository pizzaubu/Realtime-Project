from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, TeacherRegistrationForm
from kafka import KafkaProducer
from classroom.models import *
from .forms import AssignmentForm


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # เปลี่ยนไปยัง URL ของหน้าที่ต้องการหลังจากการลงทะเบียน
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/student_register.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # เปลี่ยนไปยัง URL ของหน้าที่ต้องการหลังจากการลงทะเบียน
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

def add_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teacher')  # ส่งกลับไปยังหน้าที่ต้องการหลังจากเพิ่ม Assignment เรียบร้อย
    else:
        form = AssignmentForm()

    context = {'form': form}
    return render(request, 'classroom/add_assignment.html', context)

def notify_new_course(course_id):
    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    # Send message
    producer.send('new_course_topic', value=str(course_id))
    producer.close()

def create_course(subject_name, teach_date, start_time, end_time):
    course = Course.objects.create(
        subject_name=subject_name,
        teach_date=teach_date,
        start_time=start_time,
        end_time=end_time
    )
    notify_new_course(course.id)
    return course

def student_listen_for_new_courses():
    consumer = KafkaConsumer('new_course_topic', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
    for message in consumer:
        course_id = int(message.value.decode('utf-8'))
        course = Course.objects.get(pk=course_id)
        print(f"New Course Available: {course.subject_name}")

def display_graph(request):
    # คำนวณหรือเตรียมข้อมูลที่ต้องการส่งไปแสดงใน dataframe
    # สมมติว่า dataframe_html คือสตริง HTML ที่แสดงข้อมูล dataframe
    dataframe_html = "<p>ข้อมูลที่เราต้องการแสดง (แทนที่ข้อมูลจริง)</p>"

    context = {
        'dataframe': dataframe_html
    }

    return render(request, 'graph.html', context)