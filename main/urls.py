
from django.urls import include, path


from main import views
from main.views import  dd, ZoomListView

urlpatterns = [
    path('',views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('home/', views.index, name='home_unauthenticated'),
   path('zoom/meeting/list/<int:id>', ZoomListView.as_view(), name='show_zoom_meeting_list'),

#path('zoom/meeting/create', createMeeting, name='zoom_meet_open'),
   #path('zoom/meeting/create', createMeeting, name='zoom_meet_open'),
    path('contactus/', views.contactUs, name='contact-us'),
    path('logout/', views.logoutUser, name='logout'),

]
