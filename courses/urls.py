
from django.urls import include, path


from courses.views import CoursesList, CourseCreate, CourseUpdateView, CourseDeleteView, StudentInCourse, \
    StudentAddView, course_delete, student_delete, courseUpdateView

urlpatterns = [

    path('', CoursesList.as_view(), name='courses-list'),

    path('add/', CourseCreate.as_view(), name='course-add'),
  path('<int:pk>/update/',  CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:course_id>/update/', courseUpdateView, name='course-update2'),
path('delete/',  course_delete, name='course-delete'),
    path('course/student/<int:id>', StudentInCourse.as_view(), name='student-in-course'),
    path('course/student/delete/', student_delete, name='delete-student-from-course'),
    path('course/student/add/<int:course_id>', StudentAddView.as_view(), name='add-student-to-course'),

]
