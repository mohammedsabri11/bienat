
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db import transaction

from django.forms import inlineformset_factory

from django.db.models import Avg, Count
# Create your views here.
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView

from courses.forms import BaseAnswerInlineFormSet, QuestionForm
from courses.models import Quiz, Course, Question, Answer, Episode
from main.decorators import teacher_required, admin_required
from main.forms import PasswordChangeCustomForm
from main.models import User
from student.models import Student
from teacher.form import TeacherAddForm, QuizForm, EpisoForm, ZoomForm, QuizFormUpdate

from django.views.generic import TemplateView

@method_decorator([login_required, admin_required], name='dispatch')
class TeachersList(TemplateView):
    template_name = 'teachers_list.html'

    def get_context_data(self, **kwargs):
        teachers = User.objects.filter(is_teacher=True)
        kwargs['teacher_list'] = teachers
        return super().get_context_data(**kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class TeacherAddView(CreateView):
    model = User
    form_class = TeacherAddForm
    template_name = 'add_teacher.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if self.request.method == 'POST':

            try:
                teacher = User.objects.get(name=self.request.POST['name'])
                messages.error(self.request,
                               ' خطا  اثناء عملية الاضافة يوجد استاذ اسمه ' + self.request.POST[
                                   'name'] + ' في قاعدة البيانات.')

                return super().form_invalid(form)

            except:

                form.save()
                name = self.request.POST.get('name')
                messages.success(self.request,
                                 'تم اضافة الاستاذ  ' + name + ' بنجاح.')
                return redirect('teachers-list')

    # def form_invalid(self, form):
    #     messages.error(self.request, self.error_message)
    #     return super().form_invalid(form)

@login_required
@admin_required
def teacher_delete(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.GET.get("id", None))
        name = user.name
        return JsonResponse({"valid": True, "name": name}, status=200)
    else:
        user = User.objects.get(id=request.POST.get("id", None))
        name = user.name
        user.delete()
        messages.success(request,
                         'تم حذف حساب  الاستاذة : ' + name + ' بنجاح.')
        return redirect('teachers-list')
@method_decorator([login_required, teacher_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    #context_object_name = 'quizzes'
    template_name = 'teacher_quizes_list.html'

    def get_context_data(self, **kwargs):
        kwargs['id'] = self.kwargs['id']
        episode = Episode.objects.get(id=self.kwargs['id'])
        course = Course.objects.get(teacher=self.request.user)
        queryset = Quiz.objects.filter(episode=episode,course=course)\
              .select_related('subject') \
              .annotate(questions_count=Count('questions', distinct=True)) \
              .annotate(taken_count=Count('taken_quizzes', distinct=True))
        kwargs['quizzes'] = queryset


        return super().get_context_data(**kwargs)

    # def get_queryset(self):
    #     episode = Episode.objects.get(id=self.kwargs['episode_id'])
    #     queryset = self.request.user.quizzes.filter(episode=episode) \
    #         .select_related('subject') \
    #         .annotate(questions_count=Count('questions', distinct=True)) \
    #         .annotate(taken_count=Count('taken_quizzes', distinct=True))
    #     #queryset={'quizzes':queryset}
    #     return queryset

@method_decorator([login_required, teacher_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    form_class=QuizForm
    template_name = 'quiz_add_form.html'

    def get_form_kwargs(self):
        kwargs= super(QuizCreateView,self).get_form_kwargs()
        kwargs['user']= self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['id']



        return context

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        course=Course.objects.get(teacher=self.request.user)
        episode=Episode.objects.get(id=self.kwargs['id'])
        quiz.course=course
        quiz.episode=episode
        quiz.save()
        messages.success(self.request, 'تم انشاء الاختبار بنجاح بامكانك الان اظافة اسئلة للاختبار.')
        return redirect('quiz_change',self.kwargs['id'], quiz.pk)

@method_decorator([login_required, teacher_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    form_class=QuizFormUpdate
    context_object_name = 'quiz'
    template_name = 'quiz_change_form.html'

    def get_form_kwargs(self):
        kwargs= super(QuizUpdateView,self).get_form_kwargs()
        kwargs['user']= self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        questions = self.get_object().questions.annotate(answers_count=Count('answers'))
        resu2={}
        for question in questions:

            ans = Answer.objects.filter(question=question);

            resu2.__setitem__(question, ans)
        print(resu2)
        kwargs['questions']= questions
        questionsl= Answer.objects.all();
        #     .select_related('questionsp')
        kwargs['questionsl']=questionsl
        kwargs['id'] = self.kwargs['id']
        kwargs['resu2'] = resu2
        print(questions)

        return super().get_context_data(**kwargs)


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''

        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('quiz_change', kwargs={'id':self.kwargs['id'],'pk': self.object.pk})


class StudentInCourse(ListView):
    model = Student
    context_object_name = 'student_list'
    template_name = 'student_in_teacher_course.html'

    def get_queryset(self):
        try:

          course =  Course.objects.get(teacher=self.request.user)
          queryset= Student.objects.filter(course=course)
        except:
            queryset={}
        return queryset




class EpisodeReportView(ListView):
    model = Quiz
    ordering = ('name', )
    #context_object_name = 'quizzes'
    template_name = 'student_report_course.html'

    def get_context_data(self, **kwargs):
        kwargs['id'] = self.kwargs['id']
        episode = Episode.objects.get(id=self.kwargs['id'])
        queryset = Quiz.objects.filter(episode=episode)\
              .select_related('subject') \
              .annotate(questions_count=Count('questions', distinct=True)) \
              .annotate(taken_count=Count('taken_quizzes', distinct=True))
        kwargs['quizzes'] = queryset
        context = super().get_context_data(**kwargs)
        print(queryset)
        return context

    # def get_queryset(self):
    #     episode = Episode.objects.get(id=self.kwargs['episode_id'])
    #     queryset = self.request.user.quizzes.filter(episode=episode) \
    #         .select_related('subject') \
    #         .annotate(questions_count=Count('questions', distinct=True)) \
    #         .annotate(taken_count=Count('taken_quizzes', distinct=True))
    #     #queryset={'quizzes':queryset}
    #     return queryset

# class CourseEpisodeListView(ListView):
#     model = Episode
#     ordering = ('episodeNo', )
#     context_object_name = 'courses_list'
#     template_name = 'teacher_home.html'
#
#     # def get_context_data(self, **kwargs):
#     #     course = Course.objects.get(teacher=self.request.user)
#     #     queryset = Episode.objects.filter(course=course)
#     #     print(queryset)
#     #     try:
#     #         course = Course.objects.get(teacher=self.request.user)
#     #         queryset = Episode.objects.filter(course=course)
#     #     except:
#     #         queryset = {}
#     #     kwargs['courses_list'] = queryset
#     #
#     #     # self.form_class.teacherl.queryset = teachers
#     #     return super().get_context_data(**kwargs)
#
#     def get_queryset(self):
#         course = Course.objects.get(teacher=self.request.user)
#         queryset = Episode.objects.filter(course=course)
#         return queryset
class CourseEpisodeListView(CreateView):
    model = Episode
    form_class=EpisoForm
    template_name = 'teacher_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = Course.objects.get(teacher=self.request.user)
        context['courses_list'] = Episode.objects.filter(course=course)
        context['last'] = Episode.objects.filter(course=course).order_by('id').last()


        return context

    def form_valid(self, form):
        cc = datetime.now();
        day = cc.strftime('%a');
        if not day=='Sat':
            messages.error(self.request, 'عذرا اليوم ليس السبت لذالك لاتستطيع  اضافة حلقة جديدة  ' )
            return super().form_invalid(form)

        episode = form.save(commit=False)
        course=Course.objects.get(teacher=self.request.user)
        episode_count=Episode.objects.filter(course=course).count()
        episode_count=episode_count+1
        episode.course=course
        episode.episodeNo = episode_count
        episode.save()
        messages.success(self.request, 'تم اضافة الحلقة  %s  بنجاح.' % episode_count)
        return redirect('teacher-home')



@method_decorator([login_required, teacher_required], name='dispatch')
class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

@method_decorator([login_required, admin_required], name='dispatch')
class TeacherDeleteView(DeleteView):
    model = User
    context_object_name = 'teacher'
    template_name = 'teacher_delete_confirm.html'
    success_url = reverse_lazy('teachers-list')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        messages.success(request, '   تم حذف المعلمة %s  بنجاح' % user.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        teachers = User.objects.filter(is_teacher=True)
        return teachers

@login_required
@teacher_required
def question_change(request, id,quiz_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=4,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'تم حفظ الاسئلة والاجابات بنجاح')
            return redirect('quiz_change', id,quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset,
        'id':id
    })

@login_required
@teacher_required
def question_add(request, id,pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'بامكانك الان اضافة الاجابات للسوال ')
            return redirect('question_change', id,quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'question_add_form.html', {'quiz': quiz, 'form': form,'id':id})

@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'تم حذف السوال s%  بنجاح' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('quiz_change', kwargs={'pk': question.quiz_id})

@method_decorator([login_required, teacher_required], name='dispatch')
class TeacherChangePassword(LoginRequiredMixin, TemplateView):
    form_class = PasswordChangeCustomForm
    success_message = 'تم تحديث كلمة المرور بنجاح!'
    error_message = 'خطا في تحديث كلمة المرور.'

    def get(self, request, *args, **kwargs):
        teacher = User.objects.get(id=self.request.user.id)
        form = self.form_class(self.request.user)
        return render(request, 'teacher_password_change.html', {'form': form, 'teacher': teacher})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user.username)  # Important!
            messages.success(request, self.success_message)
            return render(request, 'teacher_password_change.html', {'form': form})
        else:
            messages.error(request, self.error_message)
            return render(request, 'teacher_password_change.html', {'form': form})


