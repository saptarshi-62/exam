from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    Name=models.CharField(max_length=50)
    Email=models.EmailField()
    Username=models.CharField(max_length=50)
    Password=models.IntegerField()
    class Meta:
        db_table="Student"

class Teacher(models.Model):
    Name=models.CharField(max_length=50)
    Email=models.EmailField()
    Username=models.CharField(max_length=50)
    Password=models.IntegerField()
    class Meta:
        db_table="Teacher"

class Year(models.Model):
    year = models.CharField(max_length=4)
    def __str__(self):
        return self.year

    class Meta:
        db_table = 'Year'


class Semester(models.Model):
    semester = models.CharField(max_length=1)
    def __str__(self):
        return self.semester

    class Meta:
        db_table = 'Semester'

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=10)
    def __str__(self):
        return self.course_name

    class Meta:
        db_table = "Course"

class Mcq_question(models.Model):
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)   
    Question=models.CharField(max_length=150)
    Answer=models.CharField(max_length=500)
    Option1=models.CharField(max_length=50)
    Option2=models.CharField(max_length=50)
    Option3=models.CharField(max_length=50)
    Option4=models.CharField(max_length=50)
    QuestionNo=models.IntegerField()
    class Meta:
        db_table="MCQ"

class Theory_question(models.Model):
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Question =models.CharField(max_length=500)
    Mark=models.IntegerField()
   
    def __str__(self):
        return f"{self.Year} - {self.Semester} - {self.Course} - Theory"

    class Meta:
        db_table = "Theory"

class Exam(models.Model):
    name = models.CharField(max_length=255)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "Exam"

class Student_Response(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    theory_question=models.ForeignKey(Theory_question, on_delete=models.CASCADE)
    answer=models.TextField(blank=True)
    Mark=models.IntegerField()
    Question=models.CharField(max_length=300)
    Obtained_Mark=models.TextField(blank=True)

