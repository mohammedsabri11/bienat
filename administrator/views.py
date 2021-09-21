from collections import defaultdict

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, DeleteView

# Create your views here.
from administrator.form import AdminAddForm
from courses.models import Course, Episode, Quiz
from main.decorators import administrator_required, admin_required
from main.forms import PasswordChangeCustomForm
from main.models import User
from report.models import Score
from student.models import Student, TakenQuiz, Attendance




@login_required
@administrator_required
def admin_delete(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.GET.get("id", None))
        name = user.name
        return JsonResponse({"valid": True, "name": name}, status=200)
    else:
        user = User.objects.get(id=request.POST.get("id", None))
        name = user.name
        user.delete()
        messages.success(request,
                         'تم حذف حساب المشرفة : ' + name + ' بنجاح.')
        return redirect('admins-list')


@method_decorator([login_required, administrator_required], name='dispatch')
class AdministratorUpdate(TemplateView):
    template_name = 'admin_list.html'

@method_decorator([login_required, administrator_required], name='dispatch')
class AdministratorList(TemplateView):
    template_name = 'admin_list.html'

    def get_context_data(self, **kwargs):
        admins = User.objects.filter(is_admin=True)
        kwargs['administrator_list'] = admins
        return super().get_context_data(**kwargs)

@method_decorator([login_required, administrator_required], name='dispatch')
class AdminAddView(CreateView):
    model = User
    form_class = AdminAddForm
    template_name = 'add_admin.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if self.request.method == 'POST':

            try:
                admin = User.objects.get(name=self.request.POST['name'])
                messages.error(self.request,
                               ' خطا  اثناء عملية الاضافة يوجد مشرفة اسمه ' + self.request.POST[
                                   'name'] + ' في قاعدة البيانات.')

                return super().form_invalid(form)

            except:

                form.save()
                name = self.request.POST.get('name')
                messages.success(self.request,
                                 'تم اضافة المشرفة  ' + name + ' بنجاح.')
                return redirect('admins-list')

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


@method_decorator([login_required, admin_required], name='dispatch')
class AdminChangePassword(LoginRequiredMixin, TemplateView):
    form_class = PasswordChangeCustomForm
    success_message = 'تم تحديث كلمة المرور بنجاح!'
    error_message = 'خطا في تحديث كلمة المرور.'

    def get(self, request, *args, **kwargs):
        form = self.form_class(self.request.user)
        return render(request, 'admin_password_change.html', {'form': form, })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, self.success_message)
            return render(request, 'admin_password_change.html', {'form': form, })
        else:
            messages.error(request, self.error_message)
            return render(request, 'admin_password_change.html', {'form': form, })

@method_decorator([login_required, admin_required], name='dispatch')
class AdminCoursesListReport(TemplateView):
    template_name = 'admin_courses_report_list.html'
    def get_context_data(self, **kwargs):
        courses = Course.objects.all()\
        .annotate(student_count=Count('student_courses', distinct=True))
        kwargs['courses_list'] = courses

        #self.form_class.teacherl.queryset = teachers
        return super().get_context_data(**kwargs)

@login_required
@admin_required
def loa( request, course_id):
    course = Course.objects.get(id=course_id)
    epis = Episode.objects.filter(course=course)

    print(course)
    # form.fields['episode'].queryset = epis
    template_name = 'course_report_view.html'
    return render(request, template_name,
                  { 'episod_list': epis, 'cours_name': course.courseName, 'eee': 12})

@login_required
@admin_required
def ad_episode_report(request):
    if request.method == 'GET':
        print(request.GET)
        episode_id = request.GET.get('id', None)
        print(episode_id)
        episodeobj = Episode.objects.get(id=episode_id)
        course2 = episodeobj.course
        # course=Course.objects.get(courseName=course2)
        print(course2)
        cours_name = course2.id

        course = Course.objects.get(id=cours_name)


        students = Student.objects.filter(course=course).order_by('user_id')

        resu3 = dict(defaultdict())
        for st in students:

            resu2 = {"grammer": "-", "synomous": "-", "review": "-", "memorize": "-", "reading": "-", "num_of_faces": 0,
                     "intonation": "-"}

            try:
                QZ = TakenQuiz.objects.filter(student=st, episode=episodeobj).values('quiz', 'score')
            except:
                b = 1

            for ss in QZ:
                sub = Quiz.objects.get(id=ss['quiz'])
                subid = sub.get_subject()
                # resu2[subid].append(ss['score'])
                resu2.__setitem__(subid, ss['score'])
            try:
                studentscore = Score.objects.get(student=st, episode=episodeobj)
                resu2.__setitem__("memorize", studentscore.memorizing)
                resu2.__setitem__("reading", studentscore.reading)
                resu2.__setitem__("num_of_faces", studentscore.num_of_pages)
                resu2.__setitem__("review", studentscore.review)
            except:
                b = 1

            att = Attendance.objects.filter(student=st).count()
            resu2.__setitem__("att", att)
            resu2.__setitem__("name", st.user.name)
            resu2 = dict(resu2)
            resu3.__setitem__(st.user_id, resu2)

        resu3 = dict(resu3)

        episoded = Episode.objects.filter(course=course)

        # episoded = Episode.objects.filter(course=course)
        # kwargs['student_list'] = students
        # kwargs['epis'] = episoded
        # context['resu2'] = resu3
        # context['episode3'] = episode
        # context['cours_name'] = cours_name
        # context['epis_list'] = episoded
        #print(resu3)

        return JsonResponse({"valid": True, "resu2": resu3}, status=200)
