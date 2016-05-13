from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse

from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
#from django.template import RequestContext

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from django.contrib.auth.models import User

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    template_name = 'ccompiler/dashboard.html'
    #queryset =
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class FileList(LoginRequiredMixin, ListView):
    model = CProgram
    template_name = 'ccompiler/files.html'

class CreateProgramView(LoginRequiredMixin, CreateView):
    template_name = 'ccompiler/main.html'

class TestingSysView(LoginRequiredMixin, CreateView):
    template_name = 'ccompiler/main.html'
    form_class = SubmitProgram
    template_name = 'ccompiler/testing_system.html'