from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm
from django.forms.utils import ValidationError

from courses.models import Quiz, Course, Episode
from main.models import User
from teacher.models import Zoom


class TeacherAddForm(UserCreationForm):
    birthday = forms.DateField(
        localize=True,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        label="تاريخ الميلاد"
    )

    phone = forms.CharField(
        required=True,
        label="رقم الهاتف"
    )
    password1 = forms.CharField(label="كلمة المرور",
                                strip=False,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label="تاكيد كلمة المرور",
                                strip=False,
                                widget=forms.PasswordInput())
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','password1','password2','name','birthday','phone', )
        labels = {"name": "الاسم ",
                  "username": "اسم المستخدم",
                  "password1": "كلمة المرور",
                  "password2": "تاكيد كلمة المرور"
                  }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(TeacherAddForm, self).__init__(*args, **kwargs)


        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class QuizForm(ModelForm):

    class Meta:
        model = Quiz
        fields = ('name', 'subject',)
        labels = {"name": "العنوان :",
                  'subject': "المادة :" ,
                  }

    def __init__(self, *args, **kwargs):

        user=kwargs.pop('user')
        super(QuizForm, self).__init__(*args, **kwargs)
        # course = Course.objects.get(teacher=user)
        # espode = Episode.objects.filter(course=course)
        # self.fields['episode'].queryset = espode
        for visible in self.hidden_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def get_queryset(self,user):
        course = Course.objects.get(teacher=user)
        espode = Episode.objects.filter(course=course)
        return espode
    # def get_queryset(self):
    #     course = Course.objects.get(teacher=self.request.user)
    #     espode = Episode.objects.filter(course=course)
    #     return espode
class QuizFormUpdate(ModelForm):
    episode = forms.ModelChoiceField(
        queryset=None


    )
    class Meta:
        model = Quiz
        fields = ('name', 'subject','episode',)
        labels = {"name": "العنوان :",
                  'subject': "المادة :" ,
                  'episode': "الحلقة :" ,}

    def __init__(self, *args, **kwargs):

        user=kwargs.pop('user')
        super(QuizFormUpdate, self).__init__(*args, **kwargs)
        course = Course.objects.get(teacher=user)
        espode = Episode.objects.filter(course=course)
        self.fields['episode'].queryset = espode
        for visible in self.hidden_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def get_queryset(self,user):
        course = Course.objects.get(teacher=user)
        espode = Episode.objects.filter(course=course)
        return espode
    # def get_queryset(self):
    #     course = Course.objects.get(teacher=self.request.user)
    #     espode = Episode.objects.filter(course=course)
    #     return espode
class EpisoForm(ModelForm):

    class Meta:
        model = Episode
        exclude = ("course",)
        fields = ('course', 'episodeNo')


class ZoomForm(ModelForm):

    class Meta:
        model = Zoom

        fields = ('topic',)

        def __init__(self, *args, **kwargs):

            super(ZoomForm, self).__init__(*args, **kwargs)
            self.fields['topic'].widget.attrs['class'] = 'form-control'
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'


