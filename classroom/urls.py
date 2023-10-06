from django.urls import path
from classroom import views

urlpatterns = [
     path('', views.home, name="home"),
     path('student/', views.student, name='student'),
     path('teacher/', views.teacher, name='teacher'),
     path('add_assignment/', views.add_assignment, name='add_assignment'),
     path('student_register/', views.register_student, name='regst'),
     path('teacher_register/', views.register_teacher, name='regth'),
     path('graph/', views.display_graph, name='graph'),
     path('submit_assignment',views.submit_assignment, name='submit_assignment')
]
