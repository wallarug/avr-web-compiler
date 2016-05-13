from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, DateField, Form
from .models import *

class SubmitProgram(ModelForm):
    class Meta:
        model = CProgram
        fields = ['name', 'code_file']
