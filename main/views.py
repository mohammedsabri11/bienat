from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
#eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6Il8yU3BOZHp3UzIydUdJdmw1QlZ1S2ciLCJleHAiOjE2MzA4NzYwODMsImlhdCI6MTYzMDI3MTI4NX0.FOmrdJ_OvacJ6Vfw-Kt_iAiXExVvZYAahlS3QPHfr_Q
#
# import pyautogui as pyg
# import webbrowser as wb
# import datetime
# import time
import click
import jwt
import requests
import json
from time import time

from django.views.generic import CreateView
from zoomus import ZoomClient

from courses.models import Course, Episode
from main.forms import AuthenticationForm
from teacher.form import ZoomForm
from teacher.models import Zoom


def home(request):
    if request.user.is_authenticated:
        if  request.user.is_superuser or request.user.is_admin  :

            return render(request, 'admin_home.html')
        elif request.user.is_teacher:
            return redirect('teacher-home')

        elif request.user.is_student:
            return redirect('student-home')
        else:
            return redirect('home_unauthenticated')

    return redirect('home_unauthenticated')



def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')

    form = AuthenticationForm()
    context = {'user': form}
    return render(request, 'login3.html', context)


def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    logoutUser(request)
    return redirect('home')


def contactUs(request):
    return render(request, 'contact_us.html')



# Enter your API key and your API secret



# create a function to generate a token
# using the pyjwt library
# def generateToken(request):
#     API_KEY = '_2SpNdzwS22uGIvl5BVuKg'
#     API_SEC = 'kzKlHEVdxHukAZhQxiidC3m9KMWleydTAmh2'
#     today = datetime.today()
#     token = jwt.encode(
#
#         # Create a payload of the token containing
#         # API Key & expiration time
#         {'iss': API_KEY, 'exp': today + + timedelta(hours=1)},
#
#         # Secret used to generate token signature
#         API_SEC,
#
#         # Specify the hashing alg
#         algorithm='HS256'
#     ).decode('utf-8')
#     return token


# create json data for post requests
# meetingdetails = {"topic": "The title of your zoom meeting",
#                   "type": 2,
#                   "start_time": "2021-08-30: 12:52",
#                   "duration": "45",
#                   "timezone": "Europe/Madrid",
#                   "agenda": "test",
#
#                   "recurrence": {"type": 1,
#                                  "repeat_interval": 1
#                                  },
#                   "settings": {"host_video": "true",
#                                "participant_video": "true",
#                                "join_before_host": "False",
#                                "mute_upon_entry": "False",
#                                "watermark": "true",
#                                "audio": "voip",
#                                "auto_recording": "cloud"
#                                }
#                   }


# send a request with headers including
# a token and meeting details


import http.client
# def createMeeting2(request):
#     conn = http.client.HTTPSConnection("api.zoom.us")
#
#     headers = {
#         'authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6Il8yU3BOZHp3UzIydUdJdmw1QlZ1S2ciLCJleHAiOjE2MzA4NzYwODMsImlhdCI6MTYzMDI3MTI4NX0.FOmrdJ_OvacJ6Vfw-Kt_iAiXExVvZYAahlS3QPHfr_Q",
#         'content-type': "application/json"
#     }
#     headers = {'authorization': 'Bearer %s' % generateToken(request),
#                'content-type': 'application/json'}
#     print(generateToken(request))
#     conn.request("GET", "/v2/users?status=active&page_size=30&page_number=1", headers=headers)
#
#     res = conn.getresponse()
#     data = res.read()
#
#     print(data.decode("utf-8"))
#     return 1
#
# # run the create meeting function
# def createMeeting(request):
#     API_KEY = '_2SpNdzwS22uGIvl5BVuKg'
#     API_SEC = 'kzKlHEVdxHukAZhQxiidC3m9KMWleydTAmh2'
#     ApiKey = '_2SpNdzwS22uGIvl5BVuKg'
#     ApiSercret = 'kzKlHEVdxHukAZhQxiidC3m9KMWleydTAmh2'
#
#     today = datetime.today()
#     header = {
#         'alg': 'HS256'
#     }
#
#     payload = {
#         'iss': ApiKey,
#         'exp': today + timedelta(hours=1),
#     }
#
#     # https://docs.authlib.org/en/latest/specs/rfc7519.html#authlib.jose.rfc7519.JWT.check_sensitive_data
#     check = 'true'
#     token = jwt.encode(header, payload, ApiSercret)
#     print(token)
#     return 1


def dd(request):
    API_KEY = '_2SpNdzwS22uGIvl5BVuKg'
    API_SEC = 'kzKlHEVdxHukAZhQxiidC3m9KMWleydTAmh2'
    client = ZoomClient(API_KEY, API_SEC,version=1)

    user_list_response = client.user.list()
    user_list = json.loads(user_list_response.content)
    print(user_list_response )
    print(user_list)
    for user in user_list['users']:
        user_id = user['id']
        print(json.loads(client.meeting.list(user_id=user_id).content))


class ZoomListView(CreateView):
    model = Zoom
    form_class=ZoomForm
    template_name = 'zoom_list.html'
    error_message = 'Error saving the Student, check fields below.'

    def generateToken(self):
        API_KEY = '_2SpNdzwS22uGIvl5BVuKg'
        API_SEC = 'kzKlHEVdxHukAZhQxiidC3m9KMWleydTAmh2'
        today = datetime.today()
        token = jwt.encode(

            # Create a payload of the token containing
            # API Key & expiration time
            {'iss': API_KEY, 'exp': today + + timedelta(hours=1)},

            # Secret used to generate token signature
            API_SEC,

            # Specify the hashing alg
            algorithm='HS256'
        ).decode('utf-8')
        return token
    def createMeeting(self,topic):
        dateob=datetime.now().strftime("%Y-%m-%d %H:%M");
        print(dateob)
        meetingdetails = {"topic": topic,
                          "type": 2,
                          "start_time": dateob,
                          "duration": "45",
                          "timezone": "Europe/Madrid",
                          "agenda": "test",

                          "recurrence": {"type": 1,
                                         "repeat_interval": 1
                                         },
                          "settings": {"host_video": "False",
                                       "participant_video": "False",
                                       "join_before_host": "False",
                                       "mute_upon_entry": "False",
                                       "watermark": "true",
                                       "audio": "voip",
                                       "auto_recording": "cloud"
                                       }
                          }
        headers = {'authorization': 'Bearer %s' % self.generateToken(),
                   'content-type': 'application/json'}

        r = requests.post(
            f'https://api.zoom.us/v2/users/me/meetings',
            headers=headers, data=json.dumps(meetingdetails))

        print("\n creating zoom meeting ... \n")
        # print(r.text)
        # converting the output into json and extracting the details

        y = json.loads(r.text)
        print(y)
        join_URL = y['join_url']
        meetingPassword = y['password']

        print(
            f'\n here is your zoom meeting link {join_URL} and your \
    		password: "{meetingPassword}"\n')

        return join_URL
    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)

        course = Course.objects.get(teacher=self.request.user)
        episode = Episode.objects.filter(course=course).order_by('id').last()
        today = datetime.now();
        try:
            kwargs['zoom'] = Zoom.objects.filter(episode=episode, created_at=today).order_by('id').last()
        except :
            kwargs['zoom']=None
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        zoom = form.save(commit=False)

        zoom.join_url = self.createMeeting(zoom.topic)
        episode=  Episode.objects.get(id=self.kwargs['id'])
        zoom.episode=episode
        cc = datetime.now();
        day = cc.strftime('%a');
        zoom.day=day

        zoom.save()
        messages.success(self.request, 'تم  انشاء جلسة الزووم   بنجاح.' )
        return redirect('show_zoom_meeting_list',self.kwargs['id'])

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


#
# # functions to format date, time
# def format_date(x):
#     date_list = x.split(sep="-")
#     return list(map(int, date_list))
#
# def format_time(x):
#     time_list = x.split(sep="-")
#     return list(map(int, time_list))
#
# def given_datetime(given_date, given_time):
#
#     # YY, MM, DD, HH, MM
#     return datetime.datetime(given_date[2], given_date[1], given_date[0], given_time[0], given_time[1], given_time[2])
#
# def join_meeting(zoom_link, meeting_date, meeting_time):
#
#     meeting_date_x = format_date(meeting_date)
#     meeting_time_x = format_time(meeting_time)
#     required_datetime = given_datetime(meeting_date_x, meeting_time_x)
#
#     # time difference between current and meeting time
#     wait_time_sec = (required_datetime - datetime.datetime.now().replace(microsecond=0)).total_seconds()
#     print("Your ZOOM meeting starts in " + str(wait_time_sec/60) + " min")
#     time.sleep(wait_time_sec)
#
#     # zoom app related
#     wb.get(using='chrome').open(zoom_link, new=2) #open zoom link in a new window
#     time.sleep(5) # given time for the link to show app top-up window
#     pyg.click(x=805, y=254, clicks=1, interval=0, button='left') # click on open zoom.app option
#     time.sleep(10) # wait for 10 sec
#     pyg.click(x=195, y=31, clicks=1, interval=0, button='left') # maximize zoom app
#     time.sleep(3) # wait for 3 sec
#     pyg.click(x=50, y=776, clicks=1, interval=0, button='left')

# def join_meeting(zoom_link, meeting_date, meeting_time):
#
#
#     # time difference between current and meeting time
#
#
#     # zoom app related
#     wb.get(using='chrome').open(zoom_link, new=2) #open zoom link in a new window
#     time.sleep(5) # given time for the link to show app top-up window
#     pyg.click(x=805, y=254, clicks=1, interval=0, button='left') # click on open zoom.app option
#     time.sleep(10) # wait for 10 sec
#     pyg.click(x=195, y=31, clicks=1, interval=0, button='left') # maximize zoom app
#     time.sleep(3) # wait for 3 sec
#     pyg.click(x=50, y=776, clicks=1, interval=0, button='left')