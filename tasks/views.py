from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from tasks.models import DB_User, DB_TodoList, DB_Tasks

# Create your views here.

user = DB_User.objects.get(username="Sterling_Archer")

def view_tasks(request):
    f = open('html/tasks.html')
    template = get_template('tasks.html')
    context = Context({'todos': DB_Tasks.objects.filter(user=user.id)})
    html = template.render(context)
    return HttpResponse(html)
