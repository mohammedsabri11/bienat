"""bienat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path



from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', include('main.urls')),
    path('administrator/', include('administrator.urls')),
path('courses/', include('courses.urls')),

path('students/', include('student.urls')),
path('report/', include('report.urls')),
    path('admin/', admin.site.urls),
    path('teachers/', include('teacher.urls')),





]

urlpatterns += static(settings.CSS_URL, document_root=settings.CSS_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
