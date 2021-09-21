from django.test import TestCase

# Create your tests here.
from courses.models import Episode
from student.models import Score
episode = Episode.objects.get(id=1)
queryset = Score.objects.filter(episode=episode)
print(queryset)
            # .select_related('subject') \
            # .select_related('student')\
            # .annotate(attendance_count=Count('episode_attendance', distinct=True))

       # kwargs['quizzes'] = queryset
