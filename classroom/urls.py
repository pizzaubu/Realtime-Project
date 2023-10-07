from django.urls import path
from classroom import views

urlpatterns = [
     path('', views.home, name="home"),
     path('login/',views.log_in, name='login'),
     path('logout/', views.log_out, name='logout'),
     path('student/', views.student, name='student'),
     path('teacher/', views.teacher, name='teacher'),
     path('add_assignment/', views.add_assignment, name='add_assignment'),
     path('register/', views.register, name='register'),
     path('graph/', views.display_graph, name='graph'),
     path('submit_assignment',views.submit_assignment, name='submit_assignment'),
     path('classwork/', views.classwork, name='classwork')
]
