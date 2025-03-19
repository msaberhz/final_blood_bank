from django import forms
from django.contrib.auth.models import User
from . import models


class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PatientForm(forms.ModelForm):
    
    class Meta:
        model=models.Patient
        fields=['age','bloodgroup','disease','address','doctorname','mobile','profile_pic', 'email']


from django import forms
from .models import P_Feedback

class P_FeedbackForm(forms.ModelForm):
    class Meta:
        model = P_Feedback  # اینجا s نباید داشته باشد!
        fields = ['email', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your message here...'}),
        }


from django import forms
from .models import Patient

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['profile_pic', 'age', 'bloodgroup', 'disease', 'doctorname', 'address', 'mobile', 'email']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'bloodgroup': forms.TextInput(attrs={'class': 'form-control'}),
            'disease': forms.TextInput(attrs={'class': 'form-control'}),
            'doctorname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
