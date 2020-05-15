import math

from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from django.contrib import messages
from django.contrib.auth.models import Group
from devcal.forms import *
from .decorators import *
from .filters import *


# *****************************************#
#             Common Pages                 #
# *****************************************#


def error(request):
    context = {}
    return render(request, '404.html', context)


def home(request):
    context = {}
    return render(request, 'home.html', context)


# *****************************************#
#          login and signup pages          #
# *****************************************#
def forgotpassword(request):
    context = {}
    return render(request, 'forgot-password.html', context)


@unauthenticated_user
def signin(request):
    print(request.method)
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))

        if user is not None:
            login(request, user)
            if request.user.groups.all()[0].name == 'taskmanager':
                return redirect('tmdash')
            elif request.user.groups.all()[0].name == 'taskmember':
                return redirect('tudash')
        else:
            messages.info(request, 'username or password is incorrect')
    return render(request, 'signin.html')


def logoutu(request):
    logout(request)
    return redirect('signin')


def signup(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=role)
            user.groups.add(group)
            Duser.objects.create(user=user, )
            return redirect('signin')
    return render(request, 'signup.html', context)


# *****************************************#
#      Common Pages but with database      #
# *****************************************#
def profile(request):
    user = request.user.duser
    dform = UpdateProfile(instance=user)
    if request.method == 'POST':
        dform = UpdateProfile(request.POST, request.FILES, instance=user)
        if dform.is_valid():
            dform.save()
            redirect('tmdash')
    context = {'dform': dform}
    return render(request, 'profile.html', context)


def report(request, taskid, memberid):
    label = []
    data = []
    target = []
    taskdetails = Task.objects.get(id=taskid)
    asd = TaskReport.objects.filter(taskid_id=taskid, fillerid__user_id=memberid)
    for i in asd:
        y = str(i.fillupdate)
        label.append(y)
        x = i.reading
        data.append(x)
        z = i.taskid.target
        target.append(z)
    l2 = []
    l3 = []
    for i in range(z):
        y = (data[i] - z) ** 2
        t = (data[i] - z)
        l2.append(y)
        l3.append(t)
    dev = math.sqrt(sum(l2) / len(l2))

    context = {'labels': label, 'data': data, 'target': target, 'dev': dev, 'taskdata': asd, 'taskdetails': taskdetails,
               'dvd': l3}
    return render(request, 'report.html', context)


# *****************************************#
#             Task  Member                 #
# *****************************************#
def filltask(request, taskid, memberid):
    form = TaskFillUpForm(instance=[taskid, memberid])

    context = {}
    return render(request, 'filltask.html', context)


def tudash(request):
    user = request.user

    tinfo = TaskAssign.objects.filter(memberid=user.duser)

    ongoingtask = tinfo.filter(taskid__startdate__lte=datetime.now(), taskid__enddate__gte=datetime.now())
    oldtask = tinfo.filter(taskid__enddate__lt=datetime.now())
    futuretask = tinfo.filter(taskid__startdate__gt=datetime.now())
    ongoingtaskcount = ongoingtask.count()
    oldtaskcount = oldtask.count()
    futuretaskcount = futuretask.count()
    totaltask = futuretaskcount + oldtaskcount + ongoingtaskcount

    context = {'uinfo': user, 'tasks': tinfo, 'ongoingtask': ongoingtask, 'oldtask': oldtask,
               'futuretask': futuretask, 'oldtaskcount': oldtaskcount, 'ongoingtaskcount': ongoingtaskcount,
               'futuretaskcount': futuretaskcount, 'totaltask': totaltask}

    return render(request, 'tudash.html', context)


# *****************************************#
#             Task  Manager                #
# *****************************************#
def adduser(request, pk):
    users = Duser.objects.filter(user__groups__name='taskmember')
    print(users)
    searchfield = UserFilter(request.GET, queryset=users)
    dusers = searchfield.qs
    print(dusers)
    context = {'searchfield': searchfield, 'users': dusers, 'tid': pk}
    return render(request, 'adduser.html', context)


def assignTaskToUser(request, taskid, memberid):
    TaskAssign.objects.create(taskid_id=taskid, memberid_id=memberid)
    return redirect('tmdash')


def createtask(request):
    uinfo = request.user
    duser = uinfo.duser
    form = CreateTaskForm()
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            duser.tasks.create(**form.cleaned_data)
            return redirect('tmdash')

    context = {'form': form, 'uinfo': uinfo}
    return render(request, 'createtask.html', context)


def tmdash(request):
    user = request.user
    tinfo = Task.objects.all()

    asd = tinfo.filter(creatorid=user.duser)
    totaltask = asd.count()

    ongoingtask = asd.filter(startdate__lte=datetime.now(), enddate__gte=datetime.now())
    oldtask = asd.filter(enddate__lt=datetime.now())
    futuretask = asd.filter(startdate__gt=datetime.now())
    ongoingtaskcount = ongoingtask.count()
    oldtaskcount = oldtask.count()
    futuretaskcount = futuretask.count()

    context = {'task': asd, 'user': user, 'tinfo': tinfo, 'ongoingtask': ongoingtask, 'oldtask': oldtask,
               'futuretask': futuretask, 'oldtaskcount': oldtaskcount, 'ongoingtaskcount': ongoingtaskcount,
               'futuretaskcount': futuretaskcount, 'totaltask': totaltask}
    return render(request, 'tmdash.html', context)


def viewdetails(request, pk):
    user = request.user
    task = Task.objects.get(id=pk)
    members = task.taskmembers.all()
    context = {'task': task, 'members': members}
    return render(request, 'viewdetails.html', context)
