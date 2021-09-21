from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm

from courses.models import Course, Question, Quiz, Episode
from main.models import User
from django.forms.utils import ValidationError
from django.views.generic import ListView, CreateView

class CourseForm(ModelForm):
    teacher = forms.ModelChoiceField(
      queryset=None


       , label="المعلمة"
    )
    time_in = forms.TimeField(
        localize=True,

        widget=forms.TimeInput( attrs={'type':'time','class': 'form-control'}),
       label="وقت بدء الدرس"
    )
    time_out = forms.TimeField(
        localize=True,

        widget=forms.TimeInput(attrs={'type':'time','class': 'form-control'}),

        label="وقت انتهاء الدرس"
    )
    class Meta:
        model = Course
        exclude = ("teacher",)
        fields = ('courseName', 'teacher','time_in','time_out')
        labels = {"courseName": "اسم الكورس",
                  "teacher": "المعلمة",
                  "time_in": "بداية الدرس ",
                  "time_out": "انتهاء الدرس ",

                  }


    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = self.get_queryset()
        for visible in self.visible_fields():
              visible.field.widget.attrs['class'] = 'form-control'

    def get_queryset(self):
        teacherl = User.objects.filter(is_teacher=True)
        return teacherl

class AsignCourseTeacher(ModelForm):
    teacher = forms.ModelChoiceField(
      queryset=User.objects.filter(is_teacher=True)


       , label="المعلمة"
    )

    time_in = forms.TimeField(
        localize=True,

        widget=forms.TimeInput(format='%H:%M',attrs={'type': 'time', 'class': 'form-control'}),
        label="وقت بدء الدرس"
    )
    time_out = forms.TimeField(
        localize=True,

        widget=forms.TimeInput(format='%H:%M',attrs={'type': 'time', 'class': 'form-control'}),

        label="وقت انتهاء الدرس"
    )

    class Meta:
        model = Course
        exclude = ("teacher",)
        fields = ('courseName', 'teacher', 'time_in', 'time_out')
        labels = {"courseName": "اسم الكورس",
                  "teacher": "المعلمة",
                  "time_in": "بداية الدرس ",
                  "time_out": "انتهاء الدرس ",

                  }

    def __init__(self, *args, **kwargs):
        super(AsignCourseTeacher, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )
        labels = {"text": "السوال", }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('يجب  تحديد الاجابة الصحيحة', code='no_correct_answer')


class StudentAddForm(UserCreationForm):


    name = forms.CharField(

        required=True,label="الاسم"
    )
    birthday = forms.DateField(
        localize=True,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        label="تاريخ الميلاد"
    )

    phone = forms.CharField(
        required=True,
    label ="رقم الهاتف"
    )
    # course = forms.ModelChoiceField(
    #     queryset=Course.objects.all(),
    #
    #     required=True
    #     ,label="الحلقة التعليمية"
    # )
    password1 = forms.CharField(label="كلمة المرور" ,
                                strip=False,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label="تاكيد كلمة المرور",
                                strip=False,
                                widget=forms.PasswordInput())

    class Meta(UserCreationForm.Meta):
        model = User
        # exclude = ("course",)
        fields = (    'username', 'password1','password2',
             'name',  'phone','birthday',  )
        labels = {"username": "اسم المستخدم",
                  "password1": "كلمة المرور",
                  "password2":"تاكيد كلمة المرور"
                  }
    #    labels = { 'password1': ('كلمة المرور'), 'password2': ('تاكيد كلمة المرور'),  }

        # fields = '__all__'
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
       # user.name = self.cleaned_data.get('name'),
        user.save()
        # Student.objects.create(user=user,
        #
        #                        course=self.cleaned_data.get('course'),
        #                        )

        return user

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2



    def __init__(self,*args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)

        labels = {"الرقم التسلسلي", "الاسم", "رقم الهاتف", "اسم المستخدم", "كلمة المرور", "تاكيد كلمة المرور",
                  "تاريخ الميلاد", "الحلقة التعليمية"}
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
           # visible.field.help_text=label
           # field.label=label
        #self.u.label="اسم المستخدم"
        #self.password1.label= "كلمة المرور"
       #S self.Meta.fields['password1'].label = "كلمة المرور"

        #self.fields['password1'].label = "كلمة المرور"
        #self.user.password1.label="كلمة المرور"
        #self.user.password2.label=" تاكيد كلمة المرور"

