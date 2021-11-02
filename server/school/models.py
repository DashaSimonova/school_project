from django.contrib.auth.models import User
from django.db import models


class Classes(models.Model):
    number = models.IntegerField()
    letter = models.CharField(max_length=1, null=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Children(models.Model):
    name_rus = models.CharField(max_length=200)
    name_eng = models.CharField(max_length=200)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.ForeignKey(Classes, on_delete=models.SET_NULL, null=True)


class Applications(models.Model):
    child = models.ForeignKey(Children, on_delete=models.CASCADE)
    date = models.DateTimeField()
