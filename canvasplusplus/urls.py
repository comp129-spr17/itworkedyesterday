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
'''
* It Worked Yesterday...
* 3/20/17
* canvasplusplus.urls.py
* Links URLs to the functions that render the relevant pages.
'''
from django.conf.urls import url
from django.contrib import admin
from tasks import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/', views.updateProfile, name='profile'),
    url(r'^admin/', admin.site.urls),
    url(r'^tasks/$', views.sort_todos, {'completed_val': False}),
    url(r'^tasks/completed/$', views.sort_todos, {'completed_val': True}),
    url(r'^tasks/(.+)/$', views.sort_todos, {'completed_val': False}),
    url(r'^tasks/completed/(.+)/$', views.sort_todos, {'completed_val': True}),
    url(r'^([.+/]?)rem/([0-9]+)/([0-9]+)/$', views.removed_task),
    url(r'^([.+/]?)com/([0-9]+)/([0-9]+)/$', views.complete_task),
    url(r'^([.+/]?)edt/([0-9]+)/([0-9]+)/$', views.edit_task),
    url(r'^([.+/]?)add/([0-9]+)/([0-9]+)/$', views.add_task),
    url(r'^([.+/]?)lst/([0-9]+)/$', views.add_list),
    url(r'^([.+/]?)tasks/completed/upw/([0-9]+)/([0-9]+)/$', views.move_up, {'completed_val': True}),
    url(r'^([.+/]?)tasks/completed/dwn/([0-9]+)/([0-9]+)/$', views.move_down, {'completed_val': True}),
    url(r'^([.+/]?)upw/([0-9]+)/([0-9]+)/$', views.move_up, {'completed_val': False}),
    url(r'^([.+/]?)dwn/([0-9]+)/([0-9]+)/$', views.move_down, {'completed_val': False}),
    url(r'^fill/due/$', views.admin_func, {'func': views.fill_due}),
    url(r'^fill/ranks/$', views.admin_func, {'func': views.fill_ranks}),
    url(r'^drop/due/$', views.admin_func, {'func': views.drop_due}),
    url(r'^drop/ranks/$', views.admin_func, {'func': views.drop_ranks}),
    #password reset
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
