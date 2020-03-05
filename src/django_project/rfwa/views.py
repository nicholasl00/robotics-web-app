from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rfwa import forms
from .forms import SignUpForm, LabForm, SlideForm, FeedbackForm
from .models import Lab, Slide, Feedback
import subprocess
import os
import zipfile
from django.contrib.auth.models import User
import time
import signal
import shutil
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.http import HttpResponse

# GENERAL FEATURES


def index(request):
    return render(request, 'rfwa/home.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print("success")
            return redirect('login')
        else:
            print("form is not valid")
    else:
        form = SignUpForm()
    return render(request, 'rfwa/register.html', {'form': form})


@login_required
def lectureslides(request):
    slides = Slide.objects.order_by('name')
    return render(request, 'rfwa/lectureslides.html', {'slides': slides})


@login_required
def feedback(request):
    user = User.objects.get(username=request.user.username)
    try:
        feedbacks = Feedback.objects.filter(assignedStudent_username=user)
    except Feedback.DoesNotExist:
        feedback = None
    except ValueError:
        feedback = None
    context_dict = {'current_user': user, 'feedbacks': feedbacks}
    return render(request, 'rfwa/feedback.html', context_dict)


# labs
@login_required
def alllabs(request):
    labs = Lab.objects.order_by('open_Date')
    return render(request, 'rfwa/alllabs.html', {'labs': labs})


@login_required
def workspace(request):
    return render(request, 'rfwa/workspace.html')


@login_required
def summary(request):
    return render(request, 'rfwa/summary.html')


# ADMIN MANAGE

@login_required
def manage(request):
    if request.user.is_superuser:
        labs = Lab.objects.order_by('open_Date')
        slides = Slide.objects.order_by('name')
        users = User.objects.all()
        context_dict = {'labs': labs, 'slides': slides, 'users': users}
        return render(request, "rfwa/manage.html", context_dict)
    else:
        return redirect("index")

# labs


@login_required
def manage_labs(request):
    if request.user.is_superuser:
        labs = Lab.objects.order_by('open_Date')
    return render(request, "rfwa/manage_labs.html", {'labs': labs})


@login_required
def add_lab(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = LabForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('manage')
        else:
            form = LabForm()
        return render(request, 'rfwa/add_lab.html', {
            'form': form
        })
    else:
        return redirect("index")


@login_required
def unzip_lab(request, labName):
    try:
        lab = Lab.objects.get(slug=labName)
    except Lab.DoesNotExist:
        lab = None
    except ValueError:
        lab = None

    if lab:
        with zipfile.ZipFile(lab.lab_Files.url[1:], 'r') as zip_ref:
            print(lab.lab_Files.url[1:])
            zip_ref.extractall('../django_project/media/labs/')
    return redirect("manage")


@login_required
def delete_lab(request, labName):
    try:
        lab = Lab.objects.get(slug=labName)
    except Lab.DoesNotExist:
        lab = None
    except ValueError:
        lab = None

    # if it exists, delete it
    if lab:
        unzipped_lab = lab.lab_Files.path
        shutil.rmtree(unzipped_lab[:-4])
        os.remove(lab.lab_Files.url[1:])
        lab.delete()
    return redirect("manage")

# feedbacks


@login_required
def manage_feedback(request):
    if request.user.is_superuser:
        feedbacks = Feedback.objects.all()
    return render(request, "rfwa/manage_feedback.html", {'feedbacks': feedbacks})


@login_required
def add_feedback(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = FeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('manage')
        else:
            form = FeedbackForm()
        return render(request, 'rfwa/add_feedback.html', {
            'form': form
        })
    else:
        return redirect("index")


def delete_feedback(request, slugName):
    try:
        feedback = Feedback.objects.get(slug=slugName)
    except feedback.DoesNotExist:
        feedback = None
    except ValueError:
        feedback = None

    # if it exists, delete it
    if feedback:
        feedback.delete()
    return redirect("manage_feedback")

# slides

@login_required
def manage_slides(request):
    if request.user.is_superuser:
        slides = Slide.objects.order_by('name')
    return render(request, "rfwa/manage_slides.html", {'slides':slides})

@login_required
def add_slide(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SlideForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('manage')
        else:
            form = SlideForm()
        return render(request, 'rfwa/add_slide.html', {
            'form': form
        })
    else:
        return redirect("index")

@login_required
def delete_slide(request, slideName):
    try:
        slide = Slide.objects.get(name=slideName)
    except slide.DoesNotExist:
        slide = None
    except ValueError:
        slide = None

    # if it exists, delete it
    if slide:
        os.remove(slide.lecture_Files.url[1:])
        slide.delete()
    return redirect("manage")

# view all users

@login_required
def view_users(request):
    if request.user.is_superuser:
        users = User.objects.all()
    return render(request, "rfwa/view_users.html", {'users':users})
