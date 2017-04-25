'''
* It Worked Yesterday...
* 3/26/17
* tasks.views.py
* Renders webpages.
'''
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from tasks.models import DB_User, DB_TodoList, DB_Tasks, DB_Category, DB_Due
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from enum import Enum
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django import forms
from django.contrib.admin import widgets

from datetimewidget.widgets import DateTimeWidget
from tasks.forms import SignUpForm, ProfileForm
from canvas import add_assignments_DB, get_avatar_url

# Create your views here.

class Todos:
    def __init__(self, name, todos, id_num):
        self.name = name
        self.todos = todos
        self.id = id_num


class TasksObj:
    def __init__(self, db_task, edit_form):
        self.db_task = db_task
        self.edit_form = edit_form


class Direction(Enum):
    ASCENDING = 0
    DESCENDING = 1


class ProfileUpdate(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('login') # This is where the user will be
                                       # redirected once the form
                                       # is successfully filled in

    def get_object(self, queryset=None):
        '''This method will load the object
           that will be used to load the form
           that will be edited'''
        return self.request.user


class TaskForm(forms.Form):
    task_name = forms.CharField(label='task_name', required=True, max_length=256)
    points = forms.IntegerField(label='point', required=False)
    priority = forms.IntegerField(label='priority', required=False)
    due_date = forms.DateTimeField(label='due_date', required=False, widget=DateTimeWidget(usel10n=True, bootstrap_version=3))


class EditForm(forms.Form):
    task_name = forms.CharField(label='task_name', required=False, max_length=256)
    points = forms.IntegerField(label='point', required=False)
    priority = forms.IntegerField(label='priority', required=False)
    due_date = forms.DateTimeField(label='due_date', required=False, widget=DateTimeWidget(usel10n=True, bootstrap_version=3))


# class EditForm(forms.ModelForm):
#     class Meta:
#         model = DB_Tasks
#         fields = ['task_name', 'points', 'priority', 'end_time']
#         label = {
#             'task_name': 'task_name',
#             'points': 'points',
#             'priority': 'priority',
#             'end_time': 'due_date'
#         }
#         required = {
#             'task_name': False,
#             'points': False,
#             'priority': False,
#             'end_time': False
#         }
#         widget = {
#             'task_name': forms.TextInput,
#             'points': forms.NumberInput,
#             'priority': forms.NumberInput,
#             'end_time': DateTimeWidget(usel10n=True, bootstrap_version=3)
#         }


sorting_types = {
    "sort_by_points": "points",
    "sort_by_start_time": "start_time",
    "sort_by_due_time": "end_time",
    "sort_by_name": "task_name",
    "sort_by_priority": "priority",
    "sort_by_default": "manual_rank",
    "sort_by_manual_rank": "manual_rank"
}


def home(request):
    return redirect('/tasks/')


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
            if form.cleaned_data.get('canvas_token') != "":
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
        return HttpResponseRedirect(source)
    else:
        return HttpResponseRedirect('/tasks/')


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


def handle_due_date(task):
    try:
        existing = DB_Due.objects.get(task=task)
    except:
        existing = None
    if existing is not None:
        existing.delete()
    new = DB_Due(task=task, due=task.end_time, id=task.id)
    new.save()


def edit_task(request, source, user_id, task_id):
    if request.method == 'POST':
        selected_task = get_task(user_id, task_id)
        form = EditForm(request.POST)
        if form.is_valid():
            if selected_task is not None:
                if form.cleaned_data['task_name'] is not None and form.cleaned_data['task_name'] != "":
                    selected_task.task_name = form.cleaned_data['task_name']
                if form.cleaned_data['points'] is not None:
                    selected_task.points = form.cleaned_data['points']
                if form.cleaned_data['priority'] is not None:
                    selected_task.priority = form.cleaned_data['priority']
                if form.cleaned_data['due_date'] is not None or form.cleaned_data['due_date'] != "":
                    selected_task.end_time = form.cleaned_data['due_date']
                selected_task.save()
                if selected_task.end_time is not None:
                    handle_due_date(selected_task)
    else:
        form = EditForm()
    return sort_todos(request)


def add_task(request, source, user_id, list_id):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.cleaned_data['task_name']
            owner = DB_User.objects.get(id=user_id)
            containing_list = DB_TodoList.objects.get(id=list_id)
            category = DB_Category.objects.get(id=1)
            task = DB_Tasks(user=owner, todo_list=containing_list, task_name=new_task,
                            completed=False, points=0, point_type="Default",
                            category=category, manual_rank=get_highest_rank(containing_list)+1,
                            start_time=datetime.now(), end_time=None)
            if form.cleaned_data['points'] is not None:
                task.points = form.cleaned_data['points']
            if form.cleaned_data['priority'] is not None:
                task.priority = form.cleaned_data['priority']
            if form.cleaned_data['due_date'] is not None or form.cleaned_data['due_date'] != "":
                task.end_time = form.cleaned_data['due_date']
            task.save()
            if task.end_time is not None:
                handle_due_date(task)
    else:
        form = NameForm()
    return sort_todos(request)


def move_up(request, source, user_id, task_id, completed_val):
    selected_task = get_task(user_id, task_id)
    user = DB_User(id=user_id)
    above_tasks = DB_Tasks.objects.filter(user=user, todo_list=selected_task.todo_list, completed=completed_val).order_by('manual_rank')
    above_task = None
    for task in above_tasks:
        if task.manual_rank <= selected_task.manual_rank:
            continue
        else:
            above_task = task
            break
    if above_task is None:
        if completed_val:
            return handle_source('/tasks/completed/')
        else:
            return handle_source('/tasks/')
    if selected_task is not None:
        selected_task.manual_rank += 1
        above_task.manual_rank -= 1
        selected_task.save()
        above_task.save()
    if completed_val:
        return handle_source('/tasks/completed/')
    else:
        return handle_source('/tasks/')


def move_down(request, source, user_id, task_id, completed_val):
    selected_task = get_task(user_id, task_id)
    user = DB_User(id=user_id)
    below_tasks = DB_Tasks.objects.filter(user=user, todo_list=selected_task.todo_list, completed=completed_val).order_by('-manual_rank')
    below_task = None
    for task in below_tasks:
        if task.manual_rank >= selected_task.manual_rank:
            continue
        else:
            below_task = task
            break
    if below_task is None:
        if completed_val:
            return handle_source('/tasks/completed/')
        else:
            return handle_source('/tasks/')
    if selected_task is not None:
        selected_task.manual_rank -= 1
        below_task.manual_rank += 1
        selected_task.save()
        below_task.save()
    if completed_val:
        return handle_source('/tasks/completed/')
    else:
        return handle_source('/tasks/')

'''
Task Sorting
HOW-TO:
@key: the value of the task to sort by (ex. 'start_time')
@direction: enum of 'ascending' or 'descending'
@completed/completed_val: Boolean value whether or not you want the completed or incomplete tasks
'''

def sort_todos(request, key='sort_by_manual_rank', direction=Direction.DESCENDING, completed_val=False):
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
        new_task_form = TaskForm()
        edit_task_form = EditForm()
        for cur_list in lists:
            this_list = DB_Tasks.objects.filter(todo_list=cur_list, completed=completed_val).order_by(key)
            list_object = Todos(cur_list.name, [], cur_list.id)
            for item in this_list:
                list_object.todos.append(item)
            todos.append(list_object)

        return render(request, 'tasks.html', {'todo_lists': todos,
                                              'completed': completed_val,
                                              'in_manual_rank_mode': key == 'manual_rank' or  key == '-manual_rank',
                                              'username': user.username,
                                              'user_id': user.id,
                                              'imgurl': user.canvas_avatar_url,
                                              'new_form': new_task_form,
                                              'edit_form': edit_task_form,
                                              'list': get_template('list.html'),
                                              'lists': get_template('lists.html'),
                                              'add': get_template('add.html'),
                                              'edit': get_template('edit.html'),
                                              'sorting': get_template('sorting.html'),
                                              'individual_task': get_template('individual_task.html')})
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


def get_highest_rank(todolist):
    rank = 0
    list_of_tasks = DB_Tasks.objects.filter(todo_list=todolist)
    for item in list_of_tasks:
        if item.manual_rank is not None:
            rank = max(item.manual_rank, rank)
    return rank


def fill_in_user_ranks(user):
    list_of_lists = DB_TodoList.objects.filter(user=user)
    for todolist in list_of_lists:
        list_of_tasks = DB_Tasks.objects.filter(todo_list=todolist)
        for item in list_of_tasks:
            item.manual_rank = get_highest_rank(todolist) + 1
            item.save()


def fill_ranks(request):
    list_of_lists = DB_TodoList.objects.all()
    for todolist in list_of_lists:
        list_of_tasks = DB_Tasks.objects.filter(todo_list=todolist)
        for item in list_of_tasks:
            item.manual_rank = get_highest_rank(todolist) + 1
            item.save()
    return redirect('/admin/')


def drop_ranks(request):
    list_of_lists = DB_TodoList.objects.all()
    for todolist in list_of_lists:
        list_of_tasks = DB_Tasks.objects.filter(todo_list=todolist)
        for task in list_of_tasks:
            task.manual_rank = None
            task.save()
    return redirect('/admin/')


def drop_due(request):
    list_of_tasks = DB_Tasks.objects.all()
    for task in list_of_tasks:
        task.end_time = None
        task.save()
    return redirect('/admin/')


def fill_due(request):
    list_of_tasks = DB_Tasks.objects.all()
    for task in list_of_tasks:
        if task.end_time is not None:
            new = DB_Due(task=task, due=task.end_time, id=task.id)
            new.save()
    return redirect('/admin/')


def admin_func(request, func=None):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return func(request)
    else:
        return redirect('/login/')
