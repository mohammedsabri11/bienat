
from django.urls import include, path

from administrator import views
from administrator.views import AdministratorList, AdminAddView, AdministratorUpdate, \
    admin_delete, AdminCoursesListReport, loa,  ad_episode_report

urlpatterns = [
     path('', AdministratorList.as_view(), name='admins-list'),
path('delete/', admin_delete, name='administrator-delete'),
path('account/admin/password/update', views.AdminChangePassword.as_view(), name='admin-change-password'),


path('add', AdminAddView.as_view(), name='admin-add'),

    path('courses/report', AdminCoursesListReport.as_view(), name='admin-reports'),
    path('courses/<int:course_id>/episode/report', loa, name='admin-reports-course'),
    path('courses/episode/report/view', ad_episode_report, name='report-load'),

]
