from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from online.models import *
from django.db.models import Sum,F
from django.utils import timezone
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'teacher')

def is_student(user):
    return user.is_authenticated and hasattr(user, 'student')

def admin(request):
    return render(request, 'admin.html')

def login(request):
    return render(request, 'login.html')

def forgot_password(request):
    return render(request,'reset.html')

def reset_password(request):
    x=request.POST['Username']
    y=request.POST['Email']
    student=Student.objects.get(Email=y,Username=x)

    return render(request,'password.html',{'students':student})

def success_reset(request,student_id):
    s=Student.objects.get(id=student_id)
    s.Password=request.POST['password']
    s.save()
    return render(request,"success_reset.html")

def settheory(request):
    y=Year.objects.all()
    s=Semester.objects.all()
    c=Course.objects.all()
    return render(request, 'settheory.html',{'x':y,'a':s,'b':c})

def theory_paper(request):
    t=Theory_question.objects.all()
    return render(request,'theory_paper.html',{'q':t})

def mcq_paper(request):
    m=Mcq_question.objects.all()
    return render(request,'mcq_paper.html',{'a':m})

def setmcq(request):
    y=Year.objects.all()
    c=Course.objects.all()
    s=Semester.objects.all()
    return render(request, 'setmcq.html',{'a':y,'b':c,'d':s})

def signup(request):
    return render(request, 'signup.html')

@login_required
@user_passes_test(is_student)
def startexam(request):
    y=Year.objects.all()
    c=Course.objects.all()
    s=Semester.objects.all()
    return render(request, 'startexam.html',{'a':y,'b':c,'d':s})


def select_exam_type(request):
    course_id = request.POST.get('course_id')
    semester_id = request.POST.get('semester_id')
    year_id = request.POST.get('year_id')
    exam_type = request.POST.get('exam_type')

    if exam_type == 'theory':
        return redirect('theory_paper', course_id=course_id, semester_id=semester_id, year_id=year_id)
    elif exam_type == 'mcq':
        return redirect('mcq_paper', course_id=course_id, semester_id=semester_id, year_id=year_id)
    
    return HttpResponse('Invalid Request!Please try again')

def theory_paper(request,id):
    if request.method=='POST':
        student=request.POST.get('student_id')
        course_id = request.POST.get('course')
        exam_type = request.POST.get('exam-type')
        semester_id=request.POST.get('semester')
        if exam_type == 'mcq':
            if course_id:
                m = Mcq_question.objects.filter(Course_id=course_id,Semester_id=semester_id)
            else:
                m = Mcq_question.objects.all()
            context={
                'a':m,
                'student_id':student
            }
            return render(request, 'mcq_paper.html', context)

        elif exam_type == 'theory':
            if course_id:
                t = Theory_question.objects.filter(Course_id=course_id,Semester_id=semester_id)
            else:
                t = Theory_question.objects.all()
            context={
                'q':t,
                'student_id':student
            }
            return render(request, 'theory_paper.html', context)
        else:
            return HttpResponse('Invalid exam type')
    else:
        return HttpResponse('Invalid Request!')

def warning(request):
    return render(request, 'warning.html')

def logout(request):
    return render(request,'login.html')

def reset_button(request):
    return render(request,'reset_button.html')

def viewexam(request):
    students = Student.objects.all()
    return render(request, 'view_responses.html', {'students': students})

def view_student_exam(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    responses = Student_Response.objects.filter(student=student)
    return render(request, 'student_grades.html', {'student': student, 'responses': responses})

def leaderboard(request):
    leaderboard_data = Student_Response.objects.values('student_id').annotate(
        student_name=F('student__Name'),  # Fetch the student name
        total_obtained=Sum('Obtained_Mark'),  # Sum of obtained marks
        total_marks=Sum('Mark')     # Assuming 'Question__Mark' is available
        ).order_by('-total_obtained')  # Order by obtained marks in descending order

    return render(request, 'leaderboard.html', {'leaderboard': leaderboard_data})

def error(request):
    return render(request,'error.html')

def login1(request):
    if request.method=='POST':
        account = request.POST['account']
        if account == 'student':
            c=Course.objects.all()
            s=Semester.objects.all()
            x = request.POST['username']
            y = int(request.POST['password'])
            try:
                student=Student.objects.get(Username=x,Password=y)
            except Student.DoesNotExist:
                return redirect('error')
            student_id=student.id
            if student_id:
                context={
                    'courses':c,
                    'semesters':s,
                    'student_id':student_id
                }
                return render(request, 'startexam.html',context)
            else:
                return redirect('error')
        else:
            x = request.POST['username']
            y = int(request.POST['password'])
            if Teacher.objects.filter(Username=x, Password=y).exists():
                return render(request, 'admin.html')
            else:
                return redirect('error')
    else:
        return render(request, 'login.html')
    
def success_sign(request):
    return render(request,'success_sign.html')

def signup_code(request):
    s = Student()
    t = Teacher()
    
    account = request.POST.get('account')
    if account == 'Student':
        c=Course.objects.all()
        se=Semester.objects.all()
        s.Name = request.POST.get('Name')
        s.Email = request.POST.get('Email')
        s.Username = request.POST.get('Username')
        s.Password = request.POST.get('Password')
        s.save()
        return render(request, 'success_sign.html')
    else:
        t.Name = request.POST.get('Name')
        t.Email = request.POST.get('Email')
        t.Username = request.POST.get('Username')
        t.Password = request.POST.get('Password')
        t.save()
        return render(request, 'success_sign.html')
    
def editexam(request):
    return render(request, 'set_mcq.html')
    
def clear(request):
    Theory_question.objects.filter(year_id=1).delete() 
    return redirect('settheory')

def Add_question(request):
    year_id = request.session.get('year_id')
    semester_id = request.session.get('semester_id')
    course_id = request.session.get('course_id')
    year = Year.objects.get(id=year_id)
    semester = Semester.objects.get(id=semester_id)
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        question_a = request.POST.get('question_a')
        answer_a = request.POST.get('answer_a')
        question_b = request.POST.get('question_b')
        answer_b = request.POST.get('answer_b')
        theory_question = Theory_question(
            year=year,
            semester=semester,
            course=course,
            question_a=question_a,
            answer_a=answer_a,
            question_b=question_b,
            answer_b=answer_b
        )
        theory_question.save()
        return redirect('set_theory_question')
    return render(request, 'set_theory.html', {
        'year': year,
        'semester': semester,
        'course': course
    })

def set_mcq(request):
    m = Mcq_question()
    if request.method == 'POST':
        try:
            year_id = request.POST['year']
            semester_id = request.POST['semester']
            course_id = request.POST['course']
            request.session['year_id'] = year_id
            request.session['semester_id'] = semester_id
            request.session['course_id'] = course_id
            course = Course.objects.get(id=course_id)
            m.Year = Year.objects.get(id=year_id)
            m.Semester = Semester.objects.get(id=semester_id)
            m.Course = course 
            m.Question = request.POST.get('question')
            m.Answer = request.POST.get('answer')
            m.Option1 = request.POST.get('option1')
            m.Option2 = request.POST.get('option2')
            m.Option3 = request.POST.get('option3')
            m.Option4 = request.POST.get('option4')
            m.QuestionNo = request.POST.get('question-no')
            m.save()
            return redirect('../setmcq')
        except (Year.DoesNotExist, Semester.DoesNotExist, Course.DoesNotExist):
            return HttpResponse('Error: Foreign key instances not found')
    return render(request, 'setmcq.html')

def check_mcq(request):
    if request.method == 'POST':
        answers={}
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                question_id = int(key.split('_')[1])
                answers[question_id] = value
        request.session['user_answers']=answers
        # Compare answers with the database
        correct_answers = 0
        questions = []
        for question_id, answer in answers.items():
            question = Mcq_question.objects.get(id=question_id)
            correct = question.Answer == answer
            if correct:
                correct_answers += 1
            questions.append({
                'question': question.Question,
                'user_answer': answer,
                'correct_answer': question.Answer,
                'correct': correct
            })
        return render(request, 'results.html', {
            'questions': questions,
            'user_answer': answer,
            'correct_answers': correct_answers,
            'total_score': correct_answers / len(questions) * 100
        })
    else:
        return render(request, 'mcq_paper.html')
    
def sr(request, id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=id)
        for key, value in request.POST.items():
            if key.startswith('grade_'):
                try:
                    response_id = int(key.split('_')[1])
                    obtained_mark = float(value.strip()) if value.strip() else None
                    
                    student_response = Student_Response.objects.get(id=response_id, student=student)
                    student_response.Obtained_Mark = obtained_mark
                    student_response.save()
                    '''#Sending the mail
                    subject = "Your Exam Marks Are Now Available"
                    html_message = render_to_string('marks_submitted.html', {
                   'student_name': student.Name,
                   'teacher_name': request.user.teacher.Name if hasattr(request.user, 'teacher') else 'Your Teacher'
               })
                    plain_message = strip_tags(html_message)
                    recipient = [student.Email]
                    send_mail(subject, plain_message, None, recipient, html_message=html_message)
                    messages.success(request, "Grades submitted and student notified successfully!")'''
                except (ValueError, Student_Response.DoesNotExist):
                    messages.error(request, f"Error processing grade for response {key}")
        
        messages.success(request, "Grades submitted successfully!")
        return redirect('success_page')
    else:
        return HttpResponse("Invalid request method")

def submit_answers(request,id):
    student_id = request.POST.get('student_id')
    questions = Theory_question.objects.all()

    if request.method == 'POST':
        student = Student.objects.get(id=student_id)
        for question in questions:
            answer_text = request.POST.get(f'answer_{question.id}')
            if answer_text:
                Student_Response.objects.create(
                    student=student,
                    theory_question_id=question.id,  # Storing the question ID
                    Question=question.Question,  # Storing the question text
                    answer=answer_text,  # Storing the student's answer
                    Mark=question.Mark  # Storing the marks associated with the question
                )
        return render(request,'success.html',{
            'student_id':student,
            'Question':question,
            #'answer':answer_text
        })
    
    return render(request, 'submit_answers.html', {'questions': questions})

def success_page(request):
    return render(request, 'success.html')

def view_results(request,student_id):
    #student_id = request.GET.get('student_id')
    responses = Student_Response.objects.filter(student_id=student_id)
   
    total_marks = sum([float(response.Mark) for response in responses])
    obtained_marks = sum([float(response.Obtained_Mark) for response in responses if response.Obtained_Mark is not None])
    if total_marks > 0:
        total_score = (obtained_marks / total_marks) * 100
        total_score=round(total_score,2)
    else:
        total_score = 0
    if total_score>=90:
        grade="AA"
    elif total_score>=80:
        grade="A+"
    elif total_score>=70:
        grade="A"
    elif total_score>=60:
        grade="B"
    elif total_score>=50:
        grade="C"
    elif total_score>=40:
        grade="D"
    else:
        grade="F"
    context = {
        'q': responses,
        'total_marks': total_marks,
        'obtained_marks': obtained_marks,
        'total_score': total_score,
        'grade':grade
    }
    return render(request, 'student.html', context)

def base(request):
    return render(request, 'base.html')

def teacher(request):
    return render(request,'teacher.html')

def thanks(request):
    return HttpResponse("thanks!")

def submit_exam(request):
    current_time = timezone.now()
    end_time = datetime.fromisoformat(request.session.get('exam_end_time'))
    
    if current_time > end_time:
        # Handle late submission
        pass
    else:
        # Process the submission
        pass
    
    # Clear the timer from the session
    del request.session['exam_start_time']
    del request.session['exam_end_time']
    
    return redirect('exam_result')

def show(request):
    t = Theory_question()
    course_id = request.POST['course']
    request.session['course_id'] = course_id
    course = Course.objects.get(id=course_id)

def settheory_question(request):
        t = Theory_question()
        if request.method == 'POST':
            try:
                year_id = request.POST['year']
                semester_id = request.POST['semester']
                course_id = request.POST['course']
                request.session['year_id'] = year_id
                request.session['semester_id'] = semester_id
                request.session['course_id'] = course_id
                course = Course.objects.get(id=course_id)
                t.Year = Year.objects.get(id=year_id)
                t.Semester = Semester.objects.get(id=semester_id)
                t.Course = course 
                t.Question = request.POST.get('question')
                t.Mark = request.POST.get('mark')
                t.save()
                return redirect('../settheory')
            except (Year.DoesNotExist, Semester.DoesNotExist, Course.DoesNotExist):
                return HttpResponse('Error: Foreign key instances not found')
        return render(request, 'settheory.html')

def set_exam(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        exam_date = request.POST.get('exam_date')
        exam_time = request.POST.get('exam_time')
        duration = request.POST.get('duration')
        num_questions = int(request.POST.get('num_questions'))

        # Basic validation
        if not all([course_id, exam_date, exam_time, duration, num_questions]):
            return render(request, 'warning.html', {'message': 'All fields are required'})

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return render(request, 'warning.html', {'message': 'Course not found'})

        # Select questions from Theory_question model that were inserted through set_theory_question view
        questions = Theory_question.objects.filter(course=course, is_set=True).order_by('id')[:num_questions]

        exam = Exam(
            course=course,
            exam_date=exam_date,
            exam_time=exam_time,
            duration=duration,
            num_questions=num_questions
        )
        exam.save()
        for question in questions:
            exam.questions.add(question)

        return redirect('exam_list')
    courses = Course.objects.all()
    return render(request, 'set_exam.html', {'courses': courses})

def exam_list(request):
    course_filter = request.POST.get('course')
    exams = Exam.objects.all()
    if course_filter:
        exams = exams.filter(course__id=course_filter)
    return render(request, 'exam_list.html', {'exams': exams, 'course_filter': course_filter})

def course_input(request):
    c=Course()
    if(request.method == 'POST'):
        c.course_name=request.POST.get('course_name')
        c.course_code=request.POST.get('course_code')
        c.save()
    return render(request,'course_input.html')

def year_input(request):
    y=Year()
    if(request.method == 'POST'):
        y.year=request.POST.get('year')
        y.save()
    return render(request,'year_input.html')

def sem_input(request):
    s=Semester()
    if(request.method=='POST'):
        s.semester=request.POST.get('semester')
        s.save()
    return render(request,'sem_input.html')