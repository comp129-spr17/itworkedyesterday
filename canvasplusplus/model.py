from django.db import models


class DB_User(models.Model):
    username = models.CharField(max_length=16)
    canvas_token = models.CharField(max_length=256)
    canvas_id = models.CharField(max_length=256)
    canvas_avatar_url = models.CharField(max_length=256)


class DB_TodoList(models.Model):
    user_id = models.ForeignKey(DB_User, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=64, blank=False)
    color = models.CharField(max_length=16, blank=True)
    canvas_course_id = models.CharField(max_length=256, blank=True)
    service = models.CharField(max_length=16, blank=False)


class DB_Category(models.Model):
    name = models.CharField(max_length=256, blank=False)


class DB_Tasks(models.Model):
    list_id = models.ForeignKey(DB_TodoList, on_delete=models.CASCADE, blank=False)
    user_id = models.ForeignKey(DB_User, on_delete=models.CASCADE, blank=False)
    category_id = models.ForeignKey(DB_Category, on_delete=models.CASCADE, blank=True)
    task_name = models.CharField(max_length=64, blank=False)
    start_time = models.DateTimeField(auto_now=False, blank=True)
    end_time = models.DateTimeField(auto_now=False, blank=True)
    points = models.IntegerField(blank=True)
    point_type = models.CharField(blank=True)
    completed = models.BooleanField(blank=True)
    priority = models.IntegerField(blank=True)
    manual_rank = models.IntegerField(blank=True)
