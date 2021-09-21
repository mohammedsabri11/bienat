from django.db import models

# from courses.models import Course
# import courses
from courses.models import Course, Quiz, Answer, Episode, Subject
from main.models import User


# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_courses')
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return '{}   '.format(

            self.user.name,

        )
    # class Meta:
    #     unique_together = (('course', 'user'),)


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE, related_name='taken_quizzes')
    episode = models.ForeignKey(Episode, null=True, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='episode_attendance')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='episode_attendance')
    date = models.DateField(auto_now_add=True, auto_now=False, null=False, blank=False)
    time = models.TimeField(auto_now_add=True, auto_now=False, null=False, blank=False)
    day=models.CharField(max_length=22, null=True, blank=True)

    class Meta:
        unique_together = (( 'episode', 'student', 'date'),)


