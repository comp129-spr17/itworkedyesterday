'''
* It Worked Yesterday...
* 3/21/17
* canvasplusplus.admin.py
* Handles the admin view.
'''
from django.contrib import admin
from .models import DB_User, DB_TodoList, DB_Category, DB_Tasks, DB_Due


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'user', 'todo_list', 'start_time', 'end_time', 'points', 'completed')
    search_fields = ('task_name', )
    list_filter = ('user', )


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'canvas', 'canvas_avatar_url')
    search_fields = ('username', 'canvas')


class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'canvas_course')
    search_fields = ('name',)
    list_filter = ('owner', )


class DueAdmin(admin.ModelAdmin):
    list_filter = ('due', )


admin.site.register(DB_User, UserAdmin)
admin.site.register(DB_TodoList, ListAdmin)
admin.site.register(DB_Category)
admin.site.register(DB_Tasks, TaskAdmin)
admin.site.register(DB_Due, DueAdmin)
