from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from tasks.models import DB_User, DB_TodoList, DB_Tasks

# Create your views here.

user = DB_User.objects.get(username="Sterling_Archer")
# user = DB_User.objects.get(username="Arthur_Dent")


def view_tasks(request):
    f = open('html/tasks.html')
    template = get_template('tasks.html')
    context = Context({'todos': DB_Tasks.objects.filter(user=user.id, completed=False),
                       'username': user.username,
                       'imgurl': user.canvas_avatar_url,
                       'list': get_template('list.html')})
    html = template.render(context)
    return HttpResponse(html)


def view_completed(request):
    f = open('html/tasks.html')
    template = get_template('completed.html')
    context = Context({'todos': DB_Tasks.objects.filter(user=user.id, completed=True),
                       'username': user.username,
                       'imgurl': user.canvas_avatar_url,
                       'list': get_template('list.html')})
    html = template.render(context)
    return HttpResponse(html)


def handle_source(source):
    if source != "":
        return redirect(source)
    else:
        return redirect('/tasks/')


def create_task(user, list_id, name):
    return DB_Tasks(user=user, task_name=name, todo_list=list_id, category="Default")


def get_task(user_id, task_id):
    return DB_Tasks.objects.get(user=user_id, id=task_id)


def removed_task(request, source, user_id, task_id):
    selected_task = get_task(user_id, task_id)
    if selected_task is not None:
        selected_task.delete()
    return handle_source(source)


def complete_task(request, source, user_id, task_id):
    selected_task = get_task(user_id, task_id)
    if selected_task is not None:
        selected_task.completed = not selected_task.completed
        selected_task.save()
    return handle_source(source)


def edit_task(request, source, user_id, task_id, new_name):
    selected_task = get_task(user_id, task_id)
    if selected_task is not None:
        selected_task.task_name = new_name
        selected_task.save()
    return handle_source(source)


def add_task(request, source, user_id, list_id, new_task):
    task = DB_Tasks(user_id, list_id, new_task)
    task.save()
    return handle_source(source)

'''
Task Sorting
HOW-TO:
@key: the value of the task to sort by (ex. 'start_time')
@direction: enum of 'ascending' or 'descending'
@completed/completed_val: Boolean value whether or not you want the completed or incomplete tasks
'''

def sort_todos(key, direction, completed_val):
    f = open('html/tasks.html')
    template = get_template('tasks.html')
    if direction == 'descending':
        key = '-' + key
    elif direction == 'ascending':
        key = key
    else:
        print('Error, direction should be \'ascending\' or \'descending\'')
        key = None
    todos = DB_Tasks.objects.filter(user=user.id, completed=completed_val).order_by(k)
    context = Context({'todos': todos,
                       'username': user.username,
                       'imgurl': user.canvas_avatar_url,
                       'list': get_template('list.html')})
    html = template.render(context)
    return HttpResponse(html)


def sort_by_course(direction, completed):
    return sort_todos('todo_list',direction, completed)


# TODO: detect whether or not grading_type is by: 'points', 'letter_grade', or 'gpa_scale'
def sort_by_points(direction, completed):
    return sort_todos('points',direction, completed)


def sort_by_start_time(direction, completed):
    return sort_todos('start_time',direction, completed)


def sort_by_due_time(direction, completed):
    return sort_todos('end_time', direction, completed)


def sort_by_category(direction, completed):
    return sort_todos('category', direction, completed)

def sort_by_name(direction, completed):
    return sort_todos('name', direction, completed)

def sort_by_point_type(direction, completed):
    return sort_todos('point_type', direction, completed)

def sort_by_priority(direction, completed):
    return sort_todos('priority', direction, completed)

def sort_by_manual_rank(direction, completed):
    return sort_todos('manual_rank', direction, completed)
