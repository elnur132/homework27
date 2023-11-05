from typing import Any
from django import forms
from django.shortcuts import render, redirect
from django.forms import ValidationError, modelformset_factory
from django.urls import reverse
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name","description")
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name)<2:
            raise ValidationError('Short name, Are u from China?')
        return name

TaskFormSet = modelformset_factory(Task, form=TaskForm)

# Create your views here.
def index(request):
    
    queryset = Task.objects.all()
    
    if request.method == 'POST':
        formset = TaskFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect('main')
    
    else:
        formset = TaskFormSet(queryset=queryset)
    
    return render(request, 'index.html', {'formset':formset})