from ctypes import addressof
from django.db import models
from complaints.models import User
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from complaints.models import Category

class Employee(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length = 200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.employee.username}'
