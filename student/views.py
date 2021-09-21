from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

import student
from courses.models import Quiz, Course, Episode
from main.decorators import student_required, admin_required
from main.models import User
from student.forms import StudentAddForm, TakeQuizForm
from student.models import Student, TakenQuiz, Attendance
from report.models import Score
from teacher.models import Zoom

@method_decorator([login_required, student_required], name='dispatch')
class StudentHome(TemplateView):
    template_name = 'student_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course =Student.objects.get(user=self.request.user).course
        today = datetime.now();
        try:
            episode = Episode.objects.filter(course=course).order_by('id').last()

            zoom = Zoom.objects.filter(episode=episode, created_at=today).order_by('id').last()
            print(zoom)
            zoom_id=zoom.id
        except :
            zoom_id=0
        context['zoom_id']=zoom_id

        return context


@method_decorator([login_required, admin_required], name='dispatch')
class StudentListView(ListView):
    model = Student
    context_object_name = 'student_list'
    template_name = 'student_list.html'

    def get_queryset(self):
        # student = self.request.user.student
        queryset = Student.objects.all()
        return queryset

@method_decorator([login_required, admin_required], name='dispatch')
class StudentAddView(LoginRequiredMixin,CreateView):
    model = User
    form_class = StudentAddForm
    template_name = 'add_student.html'
    error_message = 'Error saving the Student, check fields below.'

    def get_context_data(self, **kwargs):


        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if self.request.method == 'POST':

            try:

                student = User.objects.get(name=self.request.POST['name'])
                messages.error(self.request,
                               ' خطا  اثناء عملية الاضافة يوجد طالبة اسمها ' + self.request.POST[
                                   'name'] + ' في قاعدة البيانات.')

                return super().form_invalid(form)

            except:
                form.save()

                name = self.request.POST.get('name')
                messages.success(self.request,
                                 'تم اضافة الطالبة   ' + name + ' بنجاح.')
                return redirect('students')

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

@method_decorator([login_required, admin_required], name='dispatch')
class StudentUpdateView(UpdateView):
    model = Student
    fields = ( 'course',)
    context_object_name = 'student'
    template_name = 'student_update.html'

    def get_context_data(self, **kwargs):
      #  self.fields['course'].widget.attrs['class'] = 'form-control'
        #self.fields[0].widget.attrs['class'] = 'form-control'
        print(self.fields)
        return super().get_context_data(**kwargs)


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''

        return Student.objects.all()
    def get_success_url(self):
        return reverse('students')

    # def form_invalid(self, form):
    #     messages.error(self.request, self.error_message)
    #     return super().form_invalid(form)

@login_required
@admin_required
def student_delete(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.GET.get("id", None))
        name = user.name
        return JsonResponse({"valid": True, "name": name}, status=200)
    else:
        user = User.objects.get(id=request.POST.get("id", None))
        name = user.name
        user.delete()
        messages.success(request,
                         'تم حذف حساب الطالب : ' + name + ' بنجاح.')
        return redirect('students')




@method_decorator([login_required, admin_required], name='dispatch')
class StudentDeleteView(DeleteView):
    model = User
    context_object_name = 'student'
    template_name = 'student_delete_confirm.html'
    success_url = reverse_lazy('students')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        messages.success(request, '   تم حذف الطالب %s بنجاح' % user.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        students = User.objects.all()
        return students

@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return redirect('student-home')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz,
                                                                  answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    #get_report(request, quiz, student)
                    TakenQuiz.objects.create(student=student, quiz=quiz,episode=quiz.episode,course=quiz.course, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (
                        quiz.name, score))
                    else:
                        messages.success(request,
                                         'Congratulations! You completed the quiz %s with success! You scored %s points.' % (
                                         quiz.name, score))
                    return redirect('student_quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })

def  get_report(request,quiz,student):
    subject = quiz.subject.name
    course = quiz.course
    episode = quiz.episode
    try:
        score=Score.objects.get(student=student, course=course, episode=episode)


        student_score = Score.objects.get(student=student)
    except :
        Score.objects.create(student=student, course=course, episode=episode)

@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name',)
    #context_object_name = 'quizzes'
    template_name = 'student_quiz_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        zoom_join_url = ""
        course = Student.objects.get(user=self.request.user).course
        today = datetime.now();
        try:
            episode = Episode.objects.filter(course=course).order_by('id').last()

            zoom = Zoom.objects.filter(episode=episode, created_at=today).order_by('id').last()
            zoom_id = zoom.id
        except:
            zoom_id = 0
        context['zoom_id'] = zoom_id
        student = self.request.user.student
        course = student.course
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(course=course) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)


        context['quizzes'] = queryset
        return context

    # def get_queryset(self):
    #     student = self.request.user.student
    #     course = student.course
    #     taken_quizzes = student.quizzes.values_list('pk', flat=True)
    #     try:
    #         queryset = Quiz.objects.filter(course=course) \
    #             .exclude(pk__in=taken_quizzes) \
    #             .annotate(questions_count=Count('questions')) \
    #             .filter(questions_count__gt=0)
    #     except:
    #         queryset=None
    #     print(queryset)
    #     return queryset

@login_required
@student_required
def  take_Attendance(request):
    cc = datetime.now();
    day = cc.strftime('%a');
    student=Student.objects.get(user=request.user)
    if day=='Fri':
        messages.error(request, 'عذرا اليوم هو اجازة ')
        return redirect('student-home')

    episodeid=Episode.objects.filter(course=student.course).order_by('id').last()
    #episodeid=episode.get_latest_by('id')
        #episode.objects.latest('id')


    try:
        Attendance.objects.create(student=student, day=day, episode=episodeid,created_at=cc)
        messages.success(request,
                         'تم تسجيل الحضور بنجاح')
        # Attendance.objects.get(student=student, date=cc,day=day, episode=episodeid)
       # messages.error(request, 'لقد قمت بتسجيل الحضور من قبل')
    except:
       # Attendance.objects.create(student=student, day=day, episode=episodeid)
       #  messages.success(request,
       #               'تم تسجيل الحضور بنجاح' )
        messages.error(request, 'لقد قمت بتسجيل الحضور من قبل')

    return redirect('student-home')
