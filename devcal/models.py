from django.db import models
from django.contrib.auth.models import User

# run
class Duser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,related_name='duser')
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="default.jpeg",null=True, blank=True)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    taskname = models.CharField(max_length=50, null=True)
    taskdesc = models.CharField(max_length=300, null=True)
    target = models.IntegerField(null=True)
    unit = models.CharField(max_length=50, null=True)
    startdate = models.DateField(null=True)
    enddate = models.DateField(null=True)
    duration = models.IntegerField(null=True)
    creatorid = models.ForeignKey(Duser, null=True, on_delete=models.SET_NULL, related_name='tasks')

    def __str__(self):
        return self.taskname


class TaskAssign(models.Model):
    taskid = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL,related_name='taskmembers')
    memberid = models.ForeignKey(Duser, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{} - {}'.format(self.taskid.taskname, self.memberid.user.username)


class TaskReport(models.Model):
    taskid = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)
    fillerid = models.ForeignKey(Duser, null=True, on_delete=models.SET_NULL)
    reading = models.IntegerField(null=True)
    fillupdate = models.DateField(null=True)

    def __str__(self):
        return self.taskid.taskname
