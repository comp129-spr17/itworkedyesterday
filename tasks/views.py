from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from tasks.models import DB_User, DB_TodoList, DB_Tasks

# Create your views here.

# user = DB_User.objects.get(username="Sterling_Archer")
user = DB_User.objects.get(username="Arthur_Dent")

def view_tasks(request):
    f = open('html/tasks.html')
    template = get_template('tasks.html')
    context = Context({'todos': DB_Tasks.objects.filter(user=user.id, completed=False), 'username': user.username, 'imgurl': user.canvas_avatar_url})
    html = template.render(context)
    return HttpResponse(html)


def view_completed(request):
    f = open('html/tasks.html')
    template = get_template('completed.html')
    context = Context({'todos': DB_Tasks.objects.filter(user=user.id, completed=True), 'username': user.username, 'imgurl': user.canvas_avatar_url})
    html = template.render(context)
    return HttpResponse(html)
