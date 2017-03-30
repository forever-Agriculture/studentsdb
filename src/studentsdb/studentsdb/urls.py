"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from students import views
from django.conf import settings
from django.conf.urls.static import static
from students.views import StudentUpdateView, StudentDeleteView, GroupUpdateView, GroupDeleteView, JournalView


urlpatterns = [

    # Students

    url(r'^$', views.students_list, name='home'),
    url(r'^students/add/$', views.students_add, name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

    # Groups

    url(r'^groups/$', views.groups_list, name='groups'),
    url(r'^groups/add/$', views.groups_add, name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),

    # Journal

    url(r'^journal/$', JournalView.as_view(), name='journal'),

    # Admin

    url(r'^admin/', admin.site.urls),

]   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static\
    (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
