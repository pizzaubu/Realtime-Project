from django.contrib import admin
from .models import *

# Admin class for Student
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email']

# Admin class for Teacher
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email']

# Admin class for Course
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject_name', 'teach_date', 'start_time', 'end_time']


# Admin class for CourseStudent
class CourseStudentAdmin(admin.ModelAdmin):
    list_display = ['course', 'student']

# Admin class for CourseTeacher
class CourseTeacherAdmin(admin.ModelAdmin):
    list_display = ['course', 'teacher']

# Admin class for Assignment
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'due_date', 'course']

class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'timestamp', 'submitted_file', 'remarks']

# Register the models and their corresponding admin classes
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseStudent, CourseStudentAdmin)
admin.site.register(CourseTeacher, CourseTeacherAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(AssignmentSubmission, AssignmentSubmissionAdmin)