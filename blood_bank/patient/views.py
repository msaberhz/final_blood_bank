from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels

from django.contrib import messages
from .forms import P_FeedbackForm
from .models import P_Feedback



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient
from .forms import PatientUpdateForm

@login_required
def update_patient(request):
    patient = Patient.objects.get(user=request.user)  # گرفتن اطلاعات مریض لاگین‌شده

    if request.method == "POST":
        form = PatientUpdateForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('update_patient')  # بعد از آپدیت، دوباره به همین صفحه برمی‌گردد

    else:
        form = PatientUpdateForm(instance=patient)

    return render(request, 'patient/update_patient.html', {'form': form})






@login_required
def p_feedback_view(request):
    if request.method == 'POST':
        form = P_FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()

            send_mail(
                subject=f"New Feedback from {request.user.username}",
                message= feedback.message,
                from_email = feedback.email,
                recipient_list=['afgm12626@gmail.com'],
                fail_silently = False,
            )

            messages.success(request, 'Your feedback has been sent successfully!')
            return redirect('p_feedback')
    else:
        form = P_FeedbackForm()
    return render(request, 'patient/p_feedback.html', {'form': form})








def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'patient/patientsignup.html',context=mydict)

def patient_dashboard_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),

    }
   
    return render(request,'patient/patient_dashboard.html',context=dict)




# def make_request_view(request):
#     request_form=bforms.RequestForm()
#     if request.method=='POST':
#         request_form=bforms.RequestForm(request.POST)
#         if request_form.is_valid():
#             blood_request=request_form.save(commit=False)
#             blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
#             patient= models.Patient.objects.get(user_id=request.user.id)
#             blood_request.request_by_patient=patient
#             blood_request.save()
#             return HttpResponseRedirect('my-request')  
#     return render(request,'patient/makerequest.html',{'request_form':request_form})




def make_request_view(request):
    try:
        # دریافت اطلاعات بیمار از جدول Patient
        patient = models.Patient.objects.get(user_id=request.user.id)
        
        # مقداردهی اولیه فرم با اطلاعات بیمار
        initial_data = {
            'patient_name': f"{patient.user.first_name} {patient.user.last_name}",
            'patient_age': patient.age,
            'reason': patient.disease,
            'bloodgroup': patient.bloodgroup,
        }
        request_form = bforms.RequestForm(initial=initial_data)
    except models.Patient.DoesNotExist:
        # در صورت عدم وجود اطلاعات بیمار، فرم بدون مقدار اولیه
        request_form = bforms.RequestForm()

    if request.method == 'POST':
        request_form = bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request = request_form.save(commit=False)
            blood_request.bloodgroup = request_form.cleaned_data['bloodgroup']
            blood_request.request_by_patient = patient
            blood_request.save()
            return HttpResponseRedirect('my-request')  # ریدایرکت به صفحه تاریخچه درخواست‌ها

    return render(request, 'patient/makerequest.html', {'request_form': request_form})





def my_request_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,'patient/my_request.html',{'blood_request':blood_request})
