from django.db import models

# Create your models here.
# Create your models here.
from courses.models import Episode


class Zoom(models.Model):
    join_url=models.CharField(null=True, blank=True,max_length=300)
    topic = models.CharField(max_length=300,null=True, blank=True,help_text="عنوان الجلسة")
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, blank=True,null=True, related_name='episode_zoom')
    created_at = models.DateField(auto_now_add=True, auto_now=False, null=False, blank=False)
    time = models.TimeField(auto_now_add=True, auto_now=False, null=False, blank=False)
    day = models.CharField(max_length=22, null=True, blank=True)


