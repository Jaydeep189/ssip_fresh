from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from complaints.models import User
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
    complaint = Complaint.objects.all()
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

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST,instance=request.user)
#         p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('profile')
    
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
    
#     context = {
#                 'u_form': u_form,
#                 'p_form': p_form
#               }
#     return render(request,'profile.html',context)


def comingSoon(request):
    context = {

              }
    return render(request,'coming_soon.html',context)

@login_required
def home(request):
    context = {
                'is_employee': request.user.profile.is_employee
              }
    return render(request,'index.html',context)

# new adde/
# def login_admin(request):
#     logout(request)
#     username = password = ''
#     if request.POST:
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/main/')
#     context = {
#                 "form":AdminLogin
#               }
#     return render(request,'admin_login.html', context)

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
        new_complaints = Complaint.objects.filter(status=1).first()
        completed = Complaint.objects.filter(status=3).first()
        processing = Complaint.objects.filter(status=2).first()
        context = {
            "new_complaints":new_complaints,
            "completed":completed,
            "processing":processing,
        }
        print(context)
        return render(request, 'landing/landing.html')
    else:
        return render(request, 'landing/landing.html')
        
@login_required
def NewComplaintList(request):
    if request.user.is_employee:
       new_complaints = Complaint.objects.filter(status=1)
       context = {
           "new_complaints":new_complaints,
       }
       print(context)
       return render(request, 'landing/landing.html')
    else:
        return render(request, 'landing/landing.html')
    
@login_required
def ProcessingList(request):
    if request.user.is_employee:
       processing = Complaint.objects.filter(status=2)
       context = {
            "processing":processing,
       }
       print(context)
       return render(request, 'landing/landing.html')
    else:
        return render(request, 'landing/landing.html')
    
@login_required
def CompletedList(request):
    if request.user.is_employee:
        completed = Complaint.objects.filter(status=3)
        context = {
            "completed":completed,
        }
        print(context)
        return render(request, 'landing/landing.html')
    else:
        return render(request, 'landing/landing.html')