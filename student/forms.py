from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm
from django.forms.utils import ValidationError

from courses.models import Course, Answer
from main.models import User
from .models import Student, StudentAnswer
from report.models import Score

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

    password1 = forms.CharField(label="كلمة المرور" ,
                                strip=False,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label="تاكيد كلمة المرور",
                                strip=False,
                                widget=forms.PasswordInput())

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),

        required=True
        ,label="الحلقة التعليمية"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        exclude = ("course",)
        fields = ('username', 'password1', 'password2',
                  'name', 'phone', 'birthday','course')
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
       # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        #course =self.get_queryset() #Course.objects.get(id=self.cleaned_data.get('course_id'))
        #print(self.request)
        Student.objects.create(user=user,

                               course=self.cleaned_data.get('course'),
                              )

        return user
    def get_queryset(self):
        #self.instance.
        course = Course.objects.get(id=self.cleaned_data.get('course_id'))
        return course

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

class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


