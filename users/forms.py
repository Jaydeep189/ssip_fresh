from pyexpat import model
from django import forms
# from django.contrib.auth.models import User
from complaints.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from django.db import transaction


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name=forms.CharField()
    last_name=forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# class ComplaintImageForm(forms.ModelForm):
#     class Meta:
#         model = Complaint
#         fileds = ['image']

class AdminLoginold(forms.ModelForm):
    email = forms.EmailField()
    password = forms.PasswordInput()
    class Meta:
        model = User
        fields = ['email', 'password']

# added now 6 oct 5:16pn
# class AdminRegister(forms.ModelForm):
#         # id = models.AutoField(primary_key=True)
#         first_name = forms.CharField(max_length=100)
#         email = forms.EmailField(max_length=254)
#         middle_name = forms.CharField(max_length=100)
#         last_name = forms.CharField(max_length=100)
#         # phone_no = models.IntegerField()
#         username =forms.CharField(max_length=50)
#         # category_select = forms.ChoiceField()
#         address = forms.CharField(max_length=200)
#         password=forms.CharField(widget=forms.PasswordInput())
#         confirm_password=forms.CharField(widget=forms.PasswordInput())
#     class Meta:
#         model = User
#         fields = ['username','first_name','middle_name', 'last_name', 'email', 'address','password',]
#         @transaction.atomic
#         def save(self):
#             user = super().save(commit=False)
#             user.is_employee = True
#             user.save()
#             return user
class AdminRegister(UserCreationForm):
    email = forms.EmailField()
    first_name=forms.CharField()
    last_name=forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

        @transaction.atomic
        def save(self):
            user = super().save(commit=False)
            user.is_employee = True
            user.save()
            print("THIS IS TRUE")

            return user

class AdminLogin(forms.ModelForm):
    # email = forms.EmailField()
    username =forms.CharField(max_length=50)
    password = forms.PasswordInput()
    # email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'password']