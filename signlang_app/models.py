from django.db import models

# Create your models here.

class LoginTable(models.Model):
    username=models.CharField(max_length=20, blank=True, null=True)
    password=models.CharField(max_length=20, blank=True, null=True)
    usertype=models.CharField(max_length=20, blank=True, null=True)

class UserTable(models.Model):
    name=models.CharField(max_length=20, blank=True, null=True)
    age=models.IntegerField( blank=True, null=True)
    gender=models.CharField(max_length=20, blank=True, null=True)
    email=models.CharField(max_length=50, blank=True, null=True)
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)

class ComplaintTable(models.Model):
    complaint=models.CharField(max_length=100, blank=True, null=True)
    reply=models.CharField(max_length=100, blank=True, null=True)
    date=models.DateField(auto_now_add=True, blank=True, null=True)
    USERID=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)

class FeedbackTable(models.Model):
    feedback=models.CharField(max_length=100, blank=True, null=True)
    rating=models.IntegerField( blank=True, null=True)
    date=models.DateField(auto_now_add=True, blank=True, null=True)
    USERID=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)

