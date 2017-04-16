from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.template.loader import get_template
from django.template import Context
from tasks.models import DB_User, DB_TodoList, DB_Tasks
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from enum import Enum
from canvas import add_assignments_DB, get_avatar_url
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User


from tasks.forms import SignUpForm

# Create your views here.

class Todos:
    def __init__(self, name, todos):
        self.name = name
        self.todos = todos

class Direction(Enum):
    ASCENDING = 0
    DESCENDING = 1


class ProfileUpdate(UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'profile.html'
    success_url = reverse_lazy('login') # This is where the user will be
                                       # redirected once the form
                                       # is successfully filled in

    def get_object(self, queryset=None):
        '''This method will load the object
           that will be used to load the form
           that will be edited'''
        return self.request.user

sorting_types = {
    "sort_by_points": "points",
    "sort_by_start_time": "start_time",
    "sort_by_due_time": "end_time",
    "sort_by_name": "task_name",
    "sort_by_priority": "priority",
    "sort_by_default": "manual_rank"
}


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            t = DB_User.objects.get(username=form.cleaned_data.get('username'))
            t.canvas_token = form.cleaned_data.get('canvas_token')
            t.canvas_avatar_url = get_avatar_url(form.cleaned_data.get('canvas_token'))
            t.save()
            todol = DB_TodoList.objects.get(owner=t.id)
            add_assignments_DB(todol, todol.owner, form.cleaned_data.get('canvas_token'))
            return redirect('/login/')

    else:
        form = SignUpForm()
    #if form.cleaned_data.get('token'):
        #add_assignments_DB()

    return render(request, 'signup.html', {'form': form})


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

def sort_todos(request, key, direction=Direction.ASCENDING, completed_val=False):
    if request.user.is_authenticated:
        template = get_template('tasks.html')
        user = DB_User.objects.get(user=request.user.id)
        key = sorting_types.get(key, key)
        if direction == Direction.DESCENDING:
            key = '-' + key
        elif direction == Direction.ASCENDING:
            key = key
        else:
            print('Error, direction should be \'ascending\' or \'descending\'')
            key = None
        lists = DB_TodoList.objects.filter(owner=user.id)
        todos = []
        todo_list_names = []
        i = 0
        for cur_list in lists:
            this_list = DB_Tasks.objects.filter(todo_list=cur_list, completed=completed_val)
            list_object = Todos(cur_list.name, [])
            for item in this_list:
                list_object.todos.append(item)
            todos.append(list_object)

        return render(request, 'tasks.html', {'todo_lists': todos,
                                              'completed': completed_val,
                                              'username': user.username,
                                              'imgurl': user.canvas_avatar_url,
                                              'list': get_template('list.html'),
                                              'lists': get_template('lists.html')})
    else:
        return redirect('/login/')


def sort_by_course(request, direction=Direction.ASCENDING, completed=False):
    return sort_todos(request, 'todo_list_id',direction, completed)


# TODO: detect whether or not grading_type is by: 'points', 'letter_grade', or 'gpa_scale'
def sort_by_points(request, direction=Direction.ASCENDING, completed=False):
    return sort_todos(request,'points',direction, completed)


def sort_by_start_time(request, direction=Direction.ASCENDING, completed=False):
    return sort_todos(request,'start_time',direction, completed)


def sort_by_due_time(request, direction=Direction.ASCENDING, completed=False):
    return sort_todos(request,'end_time', direction, completed)


def sort_by_category(request, direction=Direction.ASCENDING, completed=False):
    return sort_todos(request,'category', direction, completed)


def sort_by_name(request, direction=Direction.ASCENDING, completed=False):
    return sort_todos(request,'task_name', direction, completed)


def sort_by_point_type(request, direction=Direction.ASCENDING, completed=False):
    return sort_todos(request,'point_type', direction, completed)


def sort_by_priority(request, direction=Direction.ASCENDING, completed=False):
    return sort_todos(request,'priority', direction, completed)


def sort_by_manual_rank(request, direction=Direction.ASCENDING, completed=False):
    return sort_todos(request,'manual_rank', direction, completed)
