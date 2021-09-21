from django.db import models

# Create your models here.
from courses.models import Episode
from student.models import Student


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, null=False, on_delete=models.CASCADE)
    reading = models.FloatField("Reading", null=True, blank=True)
    review = models.FloatField("Review", null=True, blank=True)
    memorizing = models.FloatField("Memorizing", null=True, blank=True)

    num_of_pages = models.CharField(max_length=22, null=True, blank=True)

    class Meta:
        unique_together = (('episode', 'student'),)
