"""
URL configuration for sign_language project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from signlang_app.views import *

urlpatterns = [
    path('',Login.as_view(),name='Login'),
    path('Adminhome/',Adminhome.as_view(),name='admin_home'),
    path('Manageuser',Manageuser.as_view(),name='Manageuser'),
    path('Viewcomplaints',Viewcomplaints.as_view(),name='Viewcomplaints'),
    path('Viewfeedback',Viewfeedback.as_view(),name='Viewfeedback'),
    path('Adduser',Adduser.as_view(),name='Adduser'),
    

    path('Userhomepage',Userhomepage.as_view(),name='Userhomepage'),
    path('sendcomplaints',sendcomplaints.as_view(),name='sendcomplaints'),
    path('sendfeedback',sendfeedback.as_view(),name='sendfeedback'),
    path('Deleteuser/<int:id>',Deleteuser.as_view(),name='Deleteuser'),
    path('Deletecomplaint/<int:id>',Deletecomplaint.as_view(),name='Deletecomplaint'),
    path('Deletefeedback/<int:id>',Deletefeedback.as_view(),name='Deletefeedback'),
    path('ReplyView/<int:id>',ReplyView.as_view(),name='ReplyView'),
    path('isl/', isl_page.as_view(), name='isl_page'),
    path('video_feed/', video_feed.as_view(), name='video_feed'),
    path('StartSignAnimationView/',StartSignAnimationView.as_view(),name='StartSignAnimationView')
]
