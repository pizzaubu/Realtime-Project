from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    #id
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=300)
    email = models.EmailField()

class Teacher(models.Model):
    #id
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=300)
    email = models.EmailField()

class Course(models.Model):
    #"id": 1145200,
    subject_name = models.CharField(max_length=300)
    #"teacher_id": [1, 2],
    teach_date = models.CharField(max_length=50)
    start_time = models.CharField(max_length=6)
    end_time = models.CharField(max_length=6)

# 1 course has many students
# 1 student can attend many courses
class CourseStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE) 

# 1 course has many teacher
# 1 teacher can attend many courses 
class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) 

class Assignment(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignments/', null=True, blank=True) 