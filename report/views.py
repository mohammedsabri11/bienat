from collections import defaultdict
import datetime, time

import webbrowser as wb
from django.contrib import messages

import pyautogui as pyg
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from django.views import View
from django.views.generic import TemplateView, CreateView, ListView

from courses.models import Course, Episode, Quiz
from main.decorators import teacher_required, admin_required

from report.form import EpisodeForm,ScoreForm

from report.models import Score
from student.models import  Student, TakenQuiz, Attendance
from teacher.models import Zoom



class TeacherReportView(CreateView):
    model = Score
    form_class = ScoreForm
    template_name = 'teacher_report_view.html'


    def get_form_kwargs(self):
        kwargs= super(TeacherReportView,self).get_form_kwargs()
        course = Course.objects.get(teacher =self.request.user)
        students = Student.objects.filter(course=course).order_by('user_id')

        # epis=  Episode.objects.filter(course=course)
#        self.form_class.episode.queryset = epis
        #kwargs['epis_list']=epis
        kwargs['student_list'] = students
        return kwargs

    def get_context_data(self, **kwargs):

        course = Course.objects.get(teacher=self.request.user)

        cours_name=course.courseName
        episode=self.kwargs['id']
        students=Student.objects.filter(course=course).order_by('user_id')
        episodeobj=Episode.objects.get(id=episode)

        resu3 = dict(defaultdict())
        for st in students:

            resu2 ={"grammer": "-","synomous": "-", "review": "-","memorize":"-","reading":"-","num_of_faces": 0,"intonation":"-"}
            try:
               QZ=TakenQuiz.objects.filter(student=st,episode=episodeobj).values('quiz', 'score')
            except:
                b=1

            for ss in QZ:

                sub=Quiz.objects.get(id=ss['quiz'])
                subid=sub.get_subject()
               # resu2[subid].append(ss['score'])
                resu2.__setitem__(subid, ss['score'])
            try:
                studentscore = Score.objects.get(student=st, episode=episodeobj)
                resu2.__setitem__("memorize", studentscore.memorizing)
                resu2.__setitem__("reading", studentscore.reading)
                resu2.__setitem__("num_of_faces", studentscore.num_of_pages)
                resu2.__setitem__("review", studentscore.review)
            except:
                b=1

            att = Attendance.objects.filter(student=st).count()
            resu2.__setitem__("att", att)
            resu2.__setitem__("name",st.user.name)
            resu2 = dict(resu2)
            resu3.__setitem__(st.user_id, resu2)



        resu3= dict(resu3)

        episoded = Episode.objects.filter(course=course)

        #episoded = Episode.objects.filter(course=course)
        # kwargs['student_list'] = students
        # kwargs['epis'] = episoded
        kwargs['resu2'] = resu3
        kwargs['episode3'] = episode
        kwargs['cours_name'] = cours_name
        kwargs['epis_list'] = episoded
        kwargs['student_list'] = students
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
           score=form.save(commit=False)
           episode = self.kwargs['id']
           episodeobj = Episode.objects.get(id=episode)
           score.episode=episodeobj


           score.save()
           messages.success(self.request, 'تم اضافة علامات الطالب %s بنجاح.' % score.student.user.name)
           return redirect('episode2_report_list', self.kwargs['id'])

    def form_invalid(self, form):


        return super().form_invalid(form)

@method_decorator([login_required, admin_required], name='dispatch')
class InfoOfCourse(TemplateView):
    template_name = 'course_info.html'
    def get_context_data(self, **kwargs):
        courses = Course.objects.all()
        kwargs['courses_list'] = courses

        #self.form_class.teacherl.queryset = teachers
        return super().get_context_data(**kwargs)

class ReportCourse(View):
    template_name = 'report_day.html'
    form_class=EpisodeForm


    def get_context_data(self, **kwargs):
        courses = Course.objects.all()
        kwargs['courses_list'] = courses

        self.form_class.course_epsNo.queryset = self.get_queryset()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        course=Course.objects.get(id=self.kwargs['course_id'])
        episode = Episode.objects.filter(course=course)
        return episode

    # def get(self, request, *args, **kwargs):
    #
    #     episode = Episode.objects.get(id=request.GET.get('id'))
    #     queryset = Score.objects.filter(episode=episode) \
    #         .select_related('subject') \
    #         .select_related('student')

def episode( request,course_id):
    course = Course.objects.get(id=course_id)


    instance = Episode.objects.filter(course=course)
    print(instance)
    form =  EpisodeForm()
    form.fields['episode'].queryset=instance


    cours_name = course.courseName
    episode = "1"
    students = Student.objects.filter(course=course).order_by('user_id')

    resu3 = dict(defaultdict())
    for st in students:

        resu2 = {"grammer": "-", "review": "-", "memorize": "-", "reading": "-", "num_of_faces": 0,
                 "intonation": "-"}
        for ss in TakenQuiz.objects.filter(student_id=st.user_id).values('quiz', 'score'):
            sub = Quiz.objects.get(id=ss['quiz'])
            subid = sub.get_subject()
            # resu2[subid].append(ss['score'])
            resu2.__setitem__(subid, ss['score'])
        att = Attendance.objects.filter(student=st).count()
        resu2.__setitem__("att", att)
        resu2.__setitem__("name", st.user.name)
        resu2 = dict(resu2)
        resu3.__setitem__(st.user_id, resu2)

    resu3 = dict(resu3)
    template_name='report_day.html'


    return render(request, template_name,
                  { "form": form, "resu2": resu3, "cours_name": cours_name,
                   "episode": episode})



class ReportCour(TemplateView):
    template_name = 'teacher_home.html'

class ReportCourse2(CreateView):
    template_name = 'report_day.html'
    form_class = EpisodeForm
    model=TakenQuiz
    def get_form_kwargs(self):
        kwargs= super(ReportCourse2,self).get_form_kwargs()
        course = Course.objects.get(id=self.kwargs['course_id'])

        epis=  Episode.objects.filter(course=course)
#        self.form_class.episode.queryset = epis
        kwargs['epis']=epis

        return kwargs

    def get_context_data(self, **kwargs):

        course = Course.objects.get(id=self.kwargs['course_id'])

        epis=  Episode.objects.filter(course=course)
#        self.form_class.episode.queryset = epis
        kwargs['epis']=epis
        return super().get_context_data(**kwargs)
    def get(self, request, *args, **kwargs):

        episode = Episode.objects.get(id=self.kwargs['course_id'])

        query = TakenQuiz.objects.all().query
        query.group_by=['student_id']

        course=Course.objects.get(id=self.kwargs['course_id'])
        cours_name=course.courseName
        episode="1"
        students=Student.objects.filter(course=course).order_by('user_id')

        resu=dict(defaultdict())
        resu3 = dict(defaultdict())
        for st in students:
            resu2 = defaultdict()
            resu2 ={"grammer": "-", "review": "-","memorize":"-","reading":"-","num_of_faces": 0,"intonation":"-"}

            for ss in TakenQuiz.objects.filter(student=st).values('quiz', 'score'):

                sub=Quiz.objects.get(id=ss['quiz'])
                subid=sub.get_subject()
               # resu2[subid].append(ss['score'])
                resu2.__setitem__(subid, ss['score'])
            att = Attendance.objects.filter(student=st).count()
            resu2.__setitem__("att", att)
            resu2.__setitem__("name",st.user.name)
            resu2 = dict(resu2)
            resu3.__setitem__(st.user_id, resu2)


        resu3= dict(resu3)


        course = Course.objects.get(id=self.kwargs['course_id'])
        episoded = Episode.objects.filter(course=course)

        return render(self.request,self.template_name,{"epis":episoded,"form":self.form_class,"resu2":resu3,"cours_name":cours_name,"episode":episode})


def deacherReportCreate(request,id):
    template_name = 'attendance_report.html'
    form = ScoreForm()
    course = Course.objects.get(teacher=request.user)

    cours_name = course.courseName
    episode = id
    students = Student.objects.filter(course=course).order_by('user_id')
    episodes = Episode.objects.filter(course=course)
    form.fields['episode'].queryset = episodes
    form.fields['student'].queryset = students
    return render(request, template_name,
                  { "form": form,  "episode": episode})



def cacl_report(request,courseid,espid):
    course=Course.objects.get(id=courseid)
    student_list=Student.objects.filter(course=course)

    for student in student_list :
        sub1=TakenQuiz.objects.get(id=courseid)


class StudentTeacherReports(TemplateView):
    template_name = 'report_day.html'
    def get_context_data(self, **kwargs):
        courses = Course.objects.all()
        kwargs['courses_list'] = courses

        #self.form_class.teacherl.queryset = teachers
        return super().get_context_data(**kwargs)


class TeacherReport2(TemplateView):
    template_name = 'report_day2.html'
    form_class = EpisodeForm
    success_message = 'تم تحديث كلمة المرور بنجاح!'
    error_message = 'خطا في تحديث كلمة المرور.'


    def get(self, request, *args, **kwargs):

        course = Course.objects.get(id=self.kwargs['course_id'])
        epis = Episode.objects.filter(course=course)
        form = self.form_class(epis)
        print(epis)
        #form.fields['episode'].queryset = epis
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():

            messages.success(request, self.success_message)
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, self.error_message)
            return render(request, self.template_name, {'form': form})

@login_required
@teacher_required
def teacherAttendanceReport(request,episode_id):



    course = Course.objects.get(teacher=request.user)

    students = Student.objects.filter(course=course).order_by('user_id')
    episodeobj = Episode.objects.get(id=episode_id)

    resu3 = dict(defaultdict())
    for st in students:
        Absent = 'غ'
        resu2 = {"Sat": Absent, "Sun": Absent, "Mon": Absent, "Tue": Absent, "Wed": Absent,
                 "Thu": Absent}
        try:
            QZ = Attendance.objects.filter(student=st, episode=episodeobj).values('day')
        except:
            b = 1

        for ss in QZ:
            # resu2[subid].append(ss['score'])


             resu2.__setitem__(ss['day'], 'ح')
        try:
            att = Attendance.objects.filter(student=st, episode=episodeobj).count()
        except:
            att = 0
        resu2.__setitem__("att", att)
        resu2.__setitem__("name", st.user.name)
        resu2 = dict(resu2)
        resu3.__setitem__(st.user_id, resu2)


    # form.fields['episode'].queryset = epis
    template_name = 'attendance_report.html'
    return render(request, template_name, {'resu2': resu3, 'episode_num': episodeobj.episodeNo,'absent':Absent})

class StudentTeacherReports2(ListView):
    template_name = 'report_day.html'
    def get_context_data(self, **kwargs):
        courses = Course.objects.all()
        kwargs['courses_list'] = courses

        #self.form_class.teacherl.queryset = teachers
        return super().get_context_data(**kwargs)


def student_reports(request):

    stu=Student.objects.get(user=request.user)
    course =stu.course
    episodeobj = Episode.objects.filter(course=course)
    # course = Course.objects.get(id=cours_name)
    # print(course)



    resu3 = dict(defaultdict())
    for epis in episodeobj:

        resu2 = {"grammer": "-", "review": "-", "memorize": "-", "reading": "-", "num_of_faces": 0,
                 "intonation": "-"}
        try:
            QZ = TakenQuiz.objects.filter(student=stu, episode=epis).values('quiz', 'score')
        except:
            b = 1

        for ss in QZ:
            sub = Quiz.objects.get(id=ss['quiz'])
            subid = sub.get_subject()
            # resu2[subid].append(ss['score'])
            resu2.__setitem__(subid, ss['score'])
        try:
            studentscore = Score.objects.get(student=stu, episode=epis)
            resu2.__setitem__("memorize", studentscore.memorizing)
            resu2.__setitem__("reading", studentscore.reading)
            resu2.__setitem__("num_of_faces", studentscore.num_of_pages)
            resu2.__setitem__("review", studentscore.review)
        except:
            b = 1

        att = Attendance.objects.filter(student=stu,episode=epis).count()
        resu2.__setitem__("att", att)

        resu2 = dict(resu2)
        resu3.__setitem__(epis.episodeNo, resu2)

    resu3 = dict(resu3)


    today = datetime.datetime.now();
    try:
        episode = Episode.objects.filter(course=course).order_by('id').last()
        zoom = Zoom.objects.filter(episode=episode, created_at=today).order_by('id').last()
        zoom_id = zoom.id
    except:
        zoom_id = 0

    # episoded = Episode.objects.filter(course=course)
    # kwargs['student_list'] = students
    # kwargs['epis'] = episoded
    # context['resu2'] = resu3
    # context['episode3'] = episode
    # context['cours_name'] = cours_name
    # context['epis_list'] = episoded

    template_name = 'report_student_add_form.html'

    return render(request, template_name,
                  {  "resu2": resu3,'zoom_id':zoom_id
                  })

# functions to format date, time
def format_date(x):
    date_list = x.split(sep="-")
    return list(map(int, date_list))

def format_time(x):
    time_list = x.split(sep="-")
    return list(map(int, time_list))

def given_datetime(given_date, given_time):

    # YY, MM, DD, HH, MM
    return datetime.datetime(given_date[2], given_date[1], given_date[0], given_time[0], given_time[1], given_time[2])

def join_meeting(request,zoom_id):


    zoom = Zoom.objects.get(id=zoom_id)
    zoom_link=zoom.join_url
    meeting_date=  datetime.datetime.now().strftime("%d-%m-%Y");
    meeting_time=datetime.datetime.now().strftime("%H-%M-%S");
    meeting_date_x = format_date(meeting_date)
    meeting_time_x = format_time(meeting_time)
    required_datetime = given_datetime(meeting_date_x, meeting_time_x)

    # time difference between current and meeting time
    wait_time_sec = (required_datetime - datetime.datetime.now().replace(microsecond=0)).total_seconds()
    print("Your ZOOM meeting starts in " + str(wait_time_sec/60) + " min")
    time.sleep(wait_time_sec)

    # zoom app related
    wb.open_new(zoom_link)
    #wb.get(using='Firefox').open(zoom_link, new=2) #open zoom link in a new window
    time.sleep(5) # given time for the link to show app top-up window
    pyg.click(x=805, y=254, clicks=1, interval=0, button='left') # click on open zoom.app option
    time.sleep(10) # wait for 10 sec
    pyg.click(x=195, y=31, clicks=1, interval=0, button='left') # maximize zoom app
    time.sleep(3) # wait for 3 sec
    pyg.click(x=50, y=776, clicks=1, interval=0, button='left')


def join_meeting2(request,zoom_id):


    zoom = Zoom.objects.get(id=zoom_id)
    zoom_link=zoom.join_url
    # meeting_date=  datetime.datetime.now().strftime("%d-%m-%Y");
    # meeting_time=datetime.datetime.now().strftime("%H-%M-%S");
    # # meeting_date_x = format_date(meeting_date)
    # meeting_time_x = format_time(meeting_time)
    # required_datetime = given_datetime(meeting_date_x, meeting_time_x)
    #
    # # time difference between current and meeting time
    # wait_time_sec = (required_datetime - datetime.datetime.now().replace(microsecond=0)).total_seconds()
    # print("Your ZOOM meeting starts in " + str(wait_time_sec/60) + " min")
    # time.sleep(wait_time_sec)

    # zoom app related
    wb.open_new(zoom_link)
    #wb.get(using='Firefox').open(zoom_link, new=2) #open zoom link in a new window
    # time.sleep(5) # given time for the link to show app top-up window
    # pyg.click(x=805, y=254, clicks=1, interval=0, button='left') # click on open zoom.app option
    # time.sleep(10) # wait for 10 sec
    # pyg.click(x=195, y=31, clicks=1, interval=0, button='left') # maximize zoom app
    # time.sleep(3) # wait for 3 sec
    # pyg.click(x=50, y=776, clicks=1, interval=0, button='left')