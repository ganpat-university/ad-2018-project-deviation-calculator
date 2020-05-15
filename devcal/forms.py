from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User, Group


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['creatorid', 'duration']


class UpdateProfile(ModelForm):
    class Meta:
        model = Duser
        fields = ['profile_pic', 'phone']
        exclude = ['user']


choices = [(group.id, group.name) for group in Group.objects.all()]


class CreateUserForm(UserCreationForm):
    role = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'role', 'password1', 'password2', 'first_name', 'last_name', 'email']


class CreateTaskReport(ModelForm):
    class Meta:
        model = TaskReport
        fields = '__all__'
        exclude = ['user']


class TaskFillUpForm(ModelForm):
    class Meta:
        model = TaskAssign
        fields = '__all__'
