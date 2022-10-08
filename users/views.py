from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from complaints.models import Feedback, User
from .forms import (UserRegisterForm,
                    UserUpdateForm,
                    AdminLogin,
                    AdminRegister)
#added now
from django import forms
from django.http import *
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Employee
from complaints.models import Complaint

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
                'form' : form,
                'title' : 'Register'
              }
    return render(request,'register.html',context)


@login_required
def Complaints(request):
    if request.user.is_authenticated:
        complaint = Complaint.objects.filter(is_visible=True)
        context = {
        'complaints': complaint
        }
        return render(request, 'complaint/complaints.html', context)

@login_required
def YourComplaints(request):
    complaint = Complaint.objects.filter(user_id=request.user.id)
    user = get_object_or_404(User, pk=request.user.id)
    context = {
        'complaints' : complaint,
        'user': user
    }
    return render(request, 'complaint/your_complaints.html', context)


def admin_register(request):
    if request.method=='POST':
        form = AdminRegister(request.POST)
        if form.is_valid():
            form.save()
            admin_user = User.objects.get(username=form.cleaned_data.get('username'))
            admin_user.is_employee = True
            print(admin_user.is_employee)

            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('mainadmin-login')
    else:
        form = AdminRegister()
    context = {
                'form' : form,
                'title' : 'Register'
              }
    return render(request,'adminregister.html',context)

def admin_login(request):
    form = AdminLogin()
    if request.method == 'POST':
        form = AdminLogin(request.POST)
        # if form.is_valid():
        #     user = auth.authenticate(
        #         # username=form.cleaned_data['username'],
        #         email = form.cleaned_data['email'],
        #         password=form.cleaned_data['password'],
        #     )
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            # user = AdminUsers.objects.get(username=username)
            print(user)
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                return redirect('mainadmin-dashboard')
            else:
                message = 'Login failed!'
    return render(request, 'authentication/login.html', context={'form': form})

@login_required
def dashboard(request):
    if request.user.is_employee:
        new_complaints = Complaint.objects.filter(status=1).order_by('-id')[:4]
        completed = Complaint.objects.filter(status=3).order_by('-id')[:4]
        processing = Complaint.objects.filter(status=2).order_by('-id')[:4]
        context = {
            "new_complaints":new_complaints,
            "completed":completed,
            "processing":processing,
        }
        print(context)
        return render(request, 'dashboard/index.html', context)
    else:
        return render(request, '/')
        
@login_required
def NewComplaintList(request):
    if request.user.is_employee:
       new_complaints = Complaint.objects.filter(status=1).select_related('user_id').order_by('-id')
       context = {
           "new_complaints":new_complaints,
       }
       return render(request, 'dashboard/new-complaint-list.html', context)
    else:
        return render(request, '/')
    
@login_required
def ProcessingList(request):
    if request.user.is_employee:
       processing = Complaint.objects.filter(status=2).select_related('user_id').order_by('-id')
       context = {
            "processing":processing,
       }
       print(context)
       return render(request, 'dashboard/processing.html', context)
    else:
        return render(request, '/')
    
@login_required
def CompletedList(request):
    if request.user.is_employee:
        completed = Complaint.objects.filter(status=3).select_related('user_id').order_by('-id')
        context = {
            "completed":completed,
        }
        return render(request, 'dashboard/completed.html', context)
    else:
        return redirect('/')

@login_required
def AdminSingleComplaint(request, pk):
    if request.user.is_employee:
        complaint = get_object_or_404(Complaint, id=pk)
        user = get_object_or_404(User,id=request.user.id)
        context = {
            'complaint': complaint,
            'user' : user
        }
        return render(request, 'dashboard/single-complaint.html', context)

@login_required
def StatusChange(request, pk, status):
    print("working")
    if request.user.is_employee:
        complaint = Complaint.objects.get(pk=pk)
        complaint.status = status
        complaint.save()
        print(complaint)
        # return redirect('/dashboard/' + str(pk))
    else:
        return redirect("/")