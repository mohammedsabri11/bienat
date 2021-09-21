
from django.urls import include, path

from teacher.views import TeachersList,  TeacherAddView, StudentInCourse, QuizListView, QuizCreateView, \
    QuizUpdateView, QuizResultsView, question_add, question_change, QuestionDeleteView, CourseEpisodeListView, \
    EpisodeReportView, TeacherDeleteView, teacher_delete, TeacherChangePassword

urlpatterns = [

    path('course/info/', CourseEpisodeListView.as_view(), name='teacher-home'),
    path('home/', TeacherChangePassword.as_view(), name='teacher-change-password'),
    path('list/', TeachersList.as_view(), name='teachers-list'),
    path('delete/', teacher_delete, name='teacher-delete'),
    path('quiz/list/<int:id>/', QuizListView.as_view(), name='quiz_change_list'),
    #path('quiz/list/<int:id>/', QuizListView.as_view(), name='episode_listen_list'),
    path('quiz/add/<int:id>/', QuizCreateView.as_view(), name='quiz_add'),

    path('add/', TeacherAddView.as_view(), name='add-teacher'),
    path('<int:id>/quiz/<int:pk>/', QuizUpdateView.as_view(), name='quiz_change'),
    path('quiz/<int:pk>/results/', QuizResultsView.as_view(), name='quiz_results'),
    path('course/<int:id>/quiz/<int:pk>/question/add/',question_add, name='question_add'),
    path('course/<int:id>/quiz/<int:quiz_pk>/question/<int:question_pk>/',question_change, name='question_change'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', QuestionDeleteView.as_view(),
         name='question_delete'),

    path('course/student', StudentInCourse.as_view(), name='my-student-list'),

  ]
