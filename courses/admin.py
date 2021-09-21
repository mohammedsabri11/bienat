from django.contrib import admin

# Register your models here.

# Register your models here.
from courses.models import Episode, Course, Subject
from report.models import Score

admin.site.register(Episode)
admin.site.register(Course)
admin.site.register(Score)
admin.site.register(Subject)