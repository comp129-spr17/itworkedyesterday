'''
* It Worked Yesterday...
* 3/20/17
* tasks.models.py
* Represents all database objects as Python classes.
'''
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class DB_User(models.Model):
    username = models.CharField(max_length=16, blank=False, verbose_name ='Username')
    canvas_token = models.CharField(max_length=256, null=True, verbose_name ='Canvas Token')
    canvas = models.CharField(max_length=256, null=True, verbose_name ='Canvas ID')
    canvas_avatar_url = models.CharField(max_length=256, null=True, verbose_name ='Canvas Avatar URL')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name ='Auth User ID')
    class Meta:
        managed = True
        db_table = u'tasks_db_user'
        app_label = 'canvasplusplus'
    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        DB_User.objects.create(user=instance, id=instance.id, username=instance.username)


@receiver(post_save, sender=DB_User)
def make_default_list(sender, instance, created, **kwargs):
    if created:
        DB_TodoList.objects.create(owner=instance, name="{}'s Default List".format(instance.username), service="Default")


class DB_TodoList(models.Model):
    owner = models.ForeignKey(DB_User, on_delete=models.CASCADE, blank=False, verbose_name ='Owner ID')
    name = models.CharField(max_length=64, blank=False, verbose_name ='List Name')
    color = models.CharField(max_length=16, null=True, verbose_name ='List Color')
    canvas_course = models.CharField(max_length=256, null=True, verbose_name ='Canvas Course ID')
    service = models.CharField(max_length=16, blank=False, verbose_name ='Service')
    class Meta:
        managed = True
        db_table = u'tasks_db_todolist'
        app_label = 'canvasplusplus'
    def __str__(self):
        return self.name


class DB_Category(models.Model):
    name = models.CharField(max_length=256, blank=False)
    class Meta:
        managed = True
        db_table = u'tasks_db_category'
        app_label = 'canvasplusplus'
    def __str__(self):
        return self.name


class DB_Tasks(models.Model):
    todo_list = models.ForeignKey(DB_TodoList, on_delete=models.CASCADE, null=False, verbose_name ='List')
    user = models.ForeignKey(DB_User, on_delete=models.CASCADE, null=False, verbose_name ='Owner')
    category = models.ForeignKey(DB_Category, on_delete=models.CASCADE, null=True, verbose_name ='Category')
    task_name = models.CharField(max_length=256, null=False, verbose_name ='Task Name')
    start_time = models.DateTimeField(auto_now=True, null=True, verbose_name ='Creation Time')
    end_time = models.DateTimeField(auto_now=False, null=True, verbose_name ='Due Date')
    points = models.IntegerField(null=True, verbose_name ='Points')
    point_type = models.CharField(max_length=16, null=True, verbose_name ='Type of Points')
    completed = models.BooleanField(blank=True, verbose_name ='Is Completed?')
    priority = models.IntegerField(null=True, verbose_name ='Priority')
    manual_rank = models.IntegerField(null=True, verbose_name ='Manual Rank')
    point_priority = models.FloatField(null=True, verbose_name ='Point Priority')
    class Meta:
        managed = True
        db_table = u'tasks_db_tasks'
        app_label = 'canvasplusplus'
    def __str__(self):
        return self.task_name


class DB_Due(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    task = models.OneToOneField(DB_Tasks, verbose_name ='Task Name')
    due = models.DateTimeField(auto_now=False, null=False, verbose_name='Due Date')
    class Meta:
        managed = True
        db_table = u'tasks_db_due'
        app_label = 'canvasplusplus'
    def __str__(self):
        return str(self.id) + ": " + str(DB_Tasks.objects.get(id=self.task.id))
