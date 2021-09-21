from django.db import models
from django.utils.html import escape, mark_safe

# Create your models here.
from main.models import User


class Course(models.Model):
    teacher = models.ForeignKey(User,null=True, on_delete=models.SET_NULL, related_name='course_v',help_text="المعلمة")
    courseName = models.CharField(max_length=30, help_text= "اسم الكورس")
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    time_in=models.TimeField(null=False,auto_now_add=False,help_text="بداية الدرس")
    time_out=models.TimeField(null=False,auto_now_add=False,help_text="انتهاء الدرس")
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return '  {} '.format(

            self.courseName,

        )




class Episode(models.Model):
    course= models.ForeignKey(Course, null=True,blank=True,on_delete=models.CASCADE, related_name='courseNo')
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    episodeNo = models.IntegerField(null=True,blank=True)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return '  {} '.format(
            self.id,


        )


    def get_html_badge(self):
        name = escape(self.episodeNo)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Subject(models.Model):
    name = models.CharField(max_length=30)
    nameid=models.CharField(max_length=30,null=True,blank=True)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name


    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='quizzes')
    name    = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def get_subject(self):
        name = self.subject.nameid
        return name


def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text






