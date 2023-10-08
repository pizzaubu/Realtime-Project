from django import forms
from .models import Student, Teacher, Assignment,Course
from django.contrib.auth.forms import AuthenticationForm

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class TeacherRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    class Meta:
        model = Teacher
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'course', 'file']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class SubmitAssignmentForm(forms.ModelForm):

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "ข้อความเพิ่มเติม"}),
    )

    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )

    due_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'file', 'due_date', 'course']

        labels = {
            'title': 'ชื่อการบ้าน',
            'course':'วิชา',
            'description': 'คำอธิบาย',
            'file': 'ไฟล์การบ้าน',
            'due_date': 'วันที่ครบกำหนด',
        }


        