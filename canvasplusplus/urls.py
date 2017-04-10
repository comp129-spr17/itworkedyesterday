"""canvasplusplus URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from tasks import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^admin/', admin.site.urls),
    url(r'^tasks/$', views.sort_by_name),
   # url(r'^tasks/([.+])/((Direction.ASCENDING)|(Direction.DESCENDING))/((True)|(False)', views.sort_todos)
    url(r'^tasks/completed/$', views.view_completed),
    url(r'^([.+/]?)rem/([0-9]+)/([0-9]+)/$', views.removed_task),
    url(r'^([.+/]?)com/([0-9]+)/([0-9]+)/$', views.complete_task),
    url(r'^([.+/]?)edt/([0-9]+)/([0-9]+)$/(.+)/$', views.edit_task),
    url(r'^([.+/]?)add/([0-9]+)/([0-9]+)$/(.+)/$', views.add_task),
    url(r'^tasks/sort_by_points/$', views.sort_by_points),
    url(r'^tasks/sort_by_start_time/$', views.sort_by_start_time),
    url(r'^tasks/sort_by_due_time/$', views.sort_by_due_time),
    url(r'^tasks/sort_by_name/$', views.sort_by_name),
    url(r'^tasks/sort_by_priority/$', views.sort_by_priority)
]
