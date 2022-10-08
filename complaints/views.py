from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Complaint, Feedback
from .forms import FeedbackForm
from users.models import Employee
from .models import User


def complaint_list(request):
    if request.user.is_authenticated:
        complaint = Complaint.objects.filter(is_visible=True)
        context = {
        'complaints': complaint
        }
        return render(request, 'complaint/complaints.html', context)
    else:
        return render(request, 'landing/landing.html')


@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, id=pk)
    user = get_object_or_404(User,id=request.user.id)
    context = {
        'complaint': complaint,
        'user' : user
    }
    return render(request, 'complaint_detail.html', context)

# @login_required
# def status_change(request, pk):
#     complaint = get_object_or_404(Complaint, id=pk)
#     if request.user.profile.is_employee:
#         employee_id = Employee.objects.get(employee=request.user)
#         if employee_id != complaint.assigned_employee:
#             return HttpResponse('<h1>HTTP 403: Access Denied</h1>', status=403)

#     else:
#         if request.user != complaint.user_id:
#             return HttpResponse('<h1>HTTP 403: Access Denied</h1>', status=403)

#     form = request.POST.dict()
#     if 'Solved' in form:
#         print('Solved')
#         complaint.status = 2
#         complaint.save()
#     if 'Pending' in form:
#         print('Pending')
#         complaint.status = 1
#         complaint.save()
#     print()
#     return HttpResponseRedirect(complaint.get_absolute_url())

class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    template_name = 'complaint_create.html'
    fields = ['title', 'details','category']

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class ComplaintUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Complaint
    template_name = 'complaint_create.html'
    fields = ['title', 'details']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        complaint = self.get_object()
        if self.request.user == complaint.user_id:
            return True
        return False


class ComplaintDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Complaint
    template_name = 'complaint_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        complaint = self.get_object()
        if self.request.user == complaint.user_id:
            return True
        return False
