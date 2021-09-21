from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, DeleteView, ListView
from django.views.generic import  CreateView


# Create your views here.
from courses.forms import CourseForm, AsignCourseTeacher, StudentAddForm
from courses.models import Course, Quiz, Episode
from main.decorators import admin_required
from main.models import User
from student.models import Student
from teacher.models import Zoom

@method_decorator([login_required, admin_required], name='dispatch')
class CoursesList(TemplateView):
    template_name = 'courses_list.html'
    def get_context_data(self, **kwargs):
        courses = Course.objects.all()
        kwargs['courses_list'] = courses

        #self.form_class.teacherl.queryset = teachers
        return super().get_context_data(**kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    form_class = AsignCourseTeacher
    # fields = ('courseName', 'teacher','time_in','time_out')
    context_object_name = 'course'
    template_name = 'update_course.html'

    # def __init__(self):
    #     # teachers = User.objects.filter(is_teacher=True)
    #     # self.fields[2].queryset=teachers

    def get_context_data(self, **kwargs):

        return super().get_context_data(**kwargs)
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        if hasattr(self,'object'):
            kwargs.update({'instance':self.object})
        return kwargs

    # def get_queryset(self):
    #     '''
    #     This method is an implicit object-level permission management
    #     This view will only match the ids of existing quizzes that belongs
    #     to the logged in user.
    #     '''
    #
    #     return self.object



    def get_success_url(self):

        return reverse('courses-list')

    def form_valid(self, form):


        course=self.object
        teacher = User.objects.get(id=self.request.POST.get('teacher'))
        course.teacher=teacher
        course.courseName=self.request.POST.get('courseName')
        course.time_in= self.request.POST.get('time_in')
        course.time_out = self.request.POST.get('time_out')
        course.save()
        return super().form_valid(course)

    def form_invalid(self, form):
        print(self.request.POST)
        return super().form_invalid(form)

@method_decorator([login_required, admin_required], name='dispatch')
def courseUpdateView(request,course_id):
    if request.method=='POST':
        course = Course.objects.get(id=course_id)
        form = AsignCourseTeacher(data=request.POST, files=request.FILES,instance=course)

        if form.is_valid():
            course = Course.objects.get(id=course_id)
            teacher=User.objects.get(id=8)
            course .teacher=teacher
            course.save()
            messages.success(request,
                             'Student with Registration Id  was successfully updated.')
            return redirect('courses-list')


    course=Course.objects.get(id=course_id)
    form=AsignCourseTeacher(instance=course)
    return render(request, 'update_course.html', {

        'form': form,

    })

@method_decorator([login_required, admin_required], name='dispatch')
class CourseCreate(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'add_course.html'
    success_message = 'Course successfully created!'
    error_message = 'Error saving the Course, check fields below.'

    # success_url = reverse_lazy('courses')

    def get_context_data(self, **kwargs):
        teachers = User.objects.filter(is_teacher=True)
        kwargs['teacher'] = teachers

        #self.form_class.teacherl.queryset = teachers
        return super().get_context_data(**kwargs)



    def form_valid(self, form):

        if self.request.method == 'POST':
            print(self.request.POST)
            try:
                course = Course.objects.get(courseName=self.request.POST['courseName'])
                messages.error(self.request,
                               'Course with name ' + self.request.POST['courseName'] + ' already exists.')
                return super().form_invalid(form)
            except:
                # course=form.save()
                # TeacherCourse.objects.create(user=user,course=course )
                #
                form.save()
                name = self.request.POST.get('courseName')
                messages.success(self.request, 'Course ' + name + ' was successfully added.')
                return redirect('courses-list')

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        print(self.request.POST)
        return super().form_invalid(form)

    def get_queryset(self):
        teacherl = User.objects.filter(is_teacher=True)
        return teacherl

@method_decorator([login_required, admin_required], name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    context_object_name = 'course'
    template_name = 'course_delete_confirm.html'
    success_url = reverse_lazy('courses-list')

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        messages.success(request, '   تم حذف الكورس %s بنجاح' % course.courseName)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        course = Course.objects.all()
        return course

@method_decorator([login_required, admin_required], name='dispatch')
class StudentAddView(LoginRequiredMixin,CreateView):
    model = User
    form_class = StudentAddForm
    template_name = 'add_student_to_course.html'
    error_message = 'Error saving the Student, check fields below.'

    def get_context_data(self, **kwargs):

        kwargs['courseid'] = self.kwargs['course_id']
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if self.request.method == 'POST':

            try:

                student =   User.objects.get(name=self.request.POST['name'])
                messages.error(self.request,
                               ' خطا  اثناء عملية الاضافة يوجد طالبة اسمها ' + self.request.POST[
                                   'name'] + ' في قاعدة البيانات.')

                return super().form_invalid(form)

            except:
                user=form.save()
                # dd = StudentAddForm(data=self.request.POST, files=self.request.FILES)
                #
                course = Course.objects.get(id=self.kwargs['course_id'])

                Student.objects.create(user=user,course=course                                    )
              #  print(dd)
               # dd.save()
                name = self.request.POST.get('name')
                messages.success(self.request,
                                 'تم اضافة الطالبة   ' + name + ' بنجاح.')
                return redirect('student-in-course',self.kwargs['course_id'])

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

@method_decorator([login_required, admin_required], name='dispatch')
class StudentInCourse(ListView):
    model = Student
    context_object_name = 'student_list'
    template_name = 'student_in_course.html'

    def get_queryset(self):
        course = Course.objects.get(id=self.kwargs['id'])
        self.kwargs['course_id']=self.kwargs['id']

        students = Student.objects.filter(course=course)
        queryset={'students':students,'course_id':self.kwargs['id']}
        return queryset

@login_required
@admin_required
def course_delete(request):
    if request.method == 'GET':
        course = Course.objects.get(id=request.GET.get("id", None))
        coursename = course.courseName
        return JsonResponse({"valid": True, "name": coursename}, status=200)
    else:
        course = Course.objects.get(id=request.POST.get("id", None))
        coursename = course.courseName
        course.delete()
        messages.success(request,
                         'تم حذف الحلقة التعليمية : : ' + coursename + ' بنجاح.')
        return redirect('courses-list')

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
        student=Student.objects.get(user=user)
        course_id=student.course.pk
        user.delete()

        messages.success(request,
                         'تم حذف حساب الطالب : ' + name + ' بنجاح.')
        return redirect('student-in-course',course_id)

