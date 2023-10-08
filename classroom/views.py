from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import StudentRegistrationForm, TeacherRegistrationForm, SubmitAssignmentForm, LoginForm
from kafka import KafkaProducer
import json
from classroom.models import *
from .forms import AssignmentForm
from .kafka_producer import send_assignment_message,send_assignment_submission_message
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'student')
        
        if form_type == 'student':
            student_form = StudentRegistrationForm(request.POST)
            if student_form.is_valid():
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password'],
                    email=request.POST['email'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                )
                student = student_form.save(commit=False)
                student.user = user
                student.save()
                return redirect('home')
        else:
            teacher_form = TeacherRegistrationForm(request.POST)
            if teacher_form.is_valid():
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password'],
                    email=request.POST['email'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                )
                teacher = teacher_form.save(commit=False)
                teacher.user = user
                teacher.save()
                return redirect('home')
    else:
        student_form = StudentRegistrationForm()
        teacher_form = TeacherRegistrationForm()

    return render(request, 'classroom/register.html', {'student_form': student_form, 'teacher_form': teacher_form})



def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                
                # Check if logged in user is a teacher or student
                if Teacher.objects.filter(user=user).exists():
                    # User is a teacher
                    return redirect('teacher')  # Redirect to teacher's dashboard or any other desired URL
                elif Student.objects.filter(user=user).exists():
                    # User is a student
                    return redirect('student')  # Redirect to student's dashboard or any other desired URL
                else:
                    # This user is neither a teacher nor a student
                    return redirect('home')

            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'classroom/login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('login')

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
            assignment = form.save()

            # 2. ใช้ฟังก์ชัน send_assignment_message แทนการสร้าง Kafka producer ในฟังก์ชันนี้
            message_data = {
                'type': 'assignment',  # เพิ่ม type เพื่อระบุประเภทข้อมูล
                'assignment_id': assignment.id,
                'title': assignment.title,
                'description': assignment.description,
                'due_date': str(assignment.due_date),
                'course': assignment.course.subject_name
            }
            send_assignment_message(message_data)

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

@login_required
def submit_assignment(request):
    if request.method == 'POST':
        form = SubmitAssignmentForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Check if the user has a student profile
            if hasattr(request.user, 'student'):
                assignment = form.save(commit=False)
                assignment.student = request.user.student
                assignment.save()

                # Prepare message data for successful submission
                message = {
                    'type': 'assignment_submission',
                    'assignment_id': assignment.id,
                    'course_id': assignment.course.id,
                    'student_id': request.user.id,
                    'submitted_date': assignment.due_date.strftime('%Y-%m-%d'),
                    'file_path': assignment.file.url if assignment.file else None
                }

                # Send message to Kafka
                send_assignment_submission_message(message)

                messages.success(request, 'ส่งการบ้านสำเร็จ')  # เพิ่มข้อความแจ้งเตือนเมื่อสำเร็จ
                return redirect('home')
            else:
                messages.error(request, 'เฉพาะนักเรียนเท่านั้นที่สามารถส่งการบ้าน')
        else:
            # Prepare message data for failed submission
            fail_message = {
                'type': 'assignment_submission_failed',
                'student_id': request.user.id,
            }

            # Send failed submission message to Kafka
            send_assignment_submission_message(fail_message)

            messages.error(request, 'ส่งการบ้านไม่สำเร็จ')  # เพิ่มข้อความแจ้งเตือนเมื่อไม่สำเร็จ
            print(request.POST)
            print(form.errors)


    else:
        form = SubmitAssignmentForm()

    return render(request, 'classroom/submit_assignment.html', {'form': form})


    
def classwork(request):
    assignments = Assignment.objects.all()
    context={
        'assignments':assignments
    }
    return render(request, 'pages/classwork.html',context)