from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)



class Teacher(models.Model):
    #id
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)


class Course(models.Model):
    #"id": 1145200,
    subject_name = models.CharField(max_length=300)
    #"teacher_id": [1, 2],
    teach_date = models.CharField(max_length=50)
    start_time = models.CharField(max_length=6)
    end_time = models.CharField(max_length=6)

    def __str__(self):
        return self.subject_name

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

class AssignmentSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # เวลาที่ส่ง
    submitted_file = models.FileField(upload_to='submitted_assignments/', null=True, blank=True)  # ไฟล์การบ้านที่ส่ง
    remarks = models.TextField(null=True, blank=True)  # หมายเหตุหรือความเห็นเพิ่มเติมจากนักเรียน

    class Meta:
        unique_together = [['student', 'assignment']]  # ตรวจสอบว่านักเรียนแต่ละคนสามารถส่งการบ้านเฉพาะหนึ่งครั้งต่อหนึ่งงาน 