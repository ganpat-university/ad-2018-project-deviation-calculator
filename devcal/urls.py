from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('adduser/<str:pk>/', views.adduser, name="adduser"),
    path('assigntask/<int:taskid>/<int:memberid>', views.assignTaskToUser, name="assigntask"),
    path('createtask/', views.createtask, name="createtask"),
    path('filltask/<int:taskid>/<int:memberid>', views.filltask, name="filltask"),
    path('forgotpassword/', views.forgotpassword, name="forgotpassword"),
    path('report/<int:taskid>/<int:memberid>',views.report, name='report'),
    path('profile/', views.profile, name="profile"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('tmdash/', views.tmdash, name="tmdash"),
    path('tudash/', views.tudash, name="tudash"),
    path('viewdetails/<str:pk>/', views.viewdetails, name="viewdetails"),
    path('error/', views.error, name="error"),
    path('logout/', views.logoutu, name="logout"),
]