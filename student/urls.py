from django.urls import path

from student.views import StudentHome, StudentListView, StudentAddView, StudentUpdateView, take_quiz, StudentDeleteView, \
  student_delete, take_Attendance, QuizListView

urlpatterns = [
  path('', StudentHome.as_view(), name='student-home'),

path('student/Attendance/take', take_Attendance, name='take-attendance'),
  path('student/add/', StudentAddView.as_view(), name='add-student'),
  path('student/list/', StudentListView.as_view(), name='students'),
   # path('add/<int:course_id>', StudentAddView.as_view(), name='delete-student-from-course'),
  #path('<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
  path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
  path('delete/', student_delete, name='student-delete'),

  path('Quiz/', QuizListView.as_view(), name='student_quiz_list'),
  path('quiz/<int:pk>/', take_quiz, name='take_quiz'),

  # path('student/delete/<int:id>/', {% url 'add-student-to-course' course_id %}views.student_delete, name='student-delete'),
 # path('student/courses/list/', views.student_view_courses_list, name='student-view-courses'),
  #path('account/student/password/change', views.StudentChangePassword.as_view(), name='student-change-password'),
  #path('student/update/<int:id>/', views.updateStudent, name='student-update'),
  #path('teachers/delete/<int:instructor_id>/', lecturer_update, name='teacher-delete'),

]
