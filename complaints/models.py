from email.policy import default
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.shortcuts import get_object_or_404

class User(AbstractUser):
    is_employee = models.BooleanField(default=False)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Complaint(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name= 'Enter your complaint')
    details = models.TextField(verbose_name= 'Explain in more detail')
    date_posted = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    # assigned_employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    status_choices = [
        (1, 'Not Reviewed'),
        (2, 'Processing'),
        (3, 'Done'),
        (4, 'Rejected'),
    ]
    status = models.IntegerField(choices=status_choices, default=1)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # added now
    deadline = models.DateTimeField(auto_now_add=True, blank=True)
    is_visible = models.BooleanField(default=False)
    # ..    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('complaint-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Feedback(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=120)
    date_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return '{}-{}'.format(self.complaint.title, str(self.user.username))