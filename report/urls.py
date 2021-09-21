
from django.urls import include, path


from .views import InfoOfCourse, StudentTeacherReports, ReportCour, episode, deacherReportCreate, \
    TeacherReport2, teacherAttendanceReport, student_reports, join_meeting, \
    join_meeting2, TeacherReportView

urlpatterns = [
path('<int:id>/report/add',TeacherReportView.as_view(), name='load-teacher-episode-report'),
    path('<int:episode_id>/report/attendance', teacherAttendanceReport, name='attendanc_report_episode'),

path('courses/list/<int:course_id>', InfoOfCourse.as_view(), name='list-of-course-in-course'),
path('zoom/meeting/<int:zoom_id>/join',join_meeting2, name='zoom_meet_join'),

path('student-reports/',student_reports, name='student-reports'),

path('courses/report/student/<int:stu_id>/', StudentTeacherReports.as_view(), name='student-teacher-reports-in-course'),
]
