from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Feedback


class DonorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class DonorForm(forms.ModelForm):
    class Meta:
        model=models.Donor
        fields=['bloodgroup','address','mobile','profile_pic', 'email']

class DonationForm(forms.ModelForm):
    class Meta:
        model=models.BloodDonate
        fields=['age','bloodgroup','disease','unit']





from django import forms
from .models import Feedback  # مطمئن شوید که مدل را ایمپورت کرده‌اید

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['email', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your message here...'}),
        }


from django import forms
from django.contrib.auth.models import User
from .models import Donor

class DonorUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Donor
        fields = ['first_name', 'last_name', 'profile_pic', 'bloodgroup', 'address', 'mobile', 'email']
        widgets = {
            'bloodgroup': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        donor = super().save(commit=False)
        donor.user.first_name = self.cleaned_data['first_name']
        donor.user.last_name = self.cleaned_data['last_name']
        donor.user.save()  # ذخیره اطلاعات کاربر در مدل User
        if commit:
            donor.save()
        return donor
