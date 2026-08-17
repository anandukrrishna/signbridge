from django.forms import *

from .models import *


class UserForm(ModelForm):
    class Meta:
        model=UserTable
        fields=['name','age','gender','email']

class ComplaintForm(ModelForm):
    class Meta:
        model=ComplaintTable
        fields=['complaint']

class FeedbackForm(ModelForm):
    class Meta:
        model=FeedbackTable
        fields=['feedback','rating']

class ReplyForm(ModelForm):
    class Meta:
        model=ComplaintTable
        fields=['reply']

