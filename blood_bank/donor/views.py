from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels


from django.contrib import messages
from .forms import FeedbackForm
from . import models


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donor
from .forms import DonorUpdateForm

@login_required
def update_donor(request):
    donor = Donor.objects.get(user=request.user)  # دریافت اطلاعات Donor
    if request.method == "POST":
        form = DonorUpdateForm(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('update_donor')
    else:
        form = DonorUpdateForm(instance=donor, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })

    return render(request, 'donor/update_donor.html', {'form': form})





@login_required
def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # اختصاص کاربر لاگین‌شده
            feedback.save()

            # ارسال ایمیل به Admin
            send_mail(
                subject=f"New Feedback from {request.user.username}",
                message=feedback.message,
                from_email=feedback.email,
                recipient_list=['afgm12626@gmail.com'],  # ایمیل ادمین
                fail_silently=False,
            )

            messages.success(request, "Your feedback has been sent successfully!")
            return redirect('feedbacks')  # تغییر مسیر به صفحه اصلی

    else:
        form = FeedbackForm()

    return render(request, 'donor/feedback.html', {'form': form})








def donor_signup_view(request):
    userForm=forms.DonorUserForm()
    donorForm=forms.DonorForm()
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST)
        donorForm=forms.DonorForm(request.POST,request.FILES)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
        return HttpResponseRedirect('donorlogin')
    return render(request,'donor/donorsignup.html',context=mydict)


def donor_dashboard_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Rejected').count(),
    }
    return render(request,'donor/donor_dashboard.html',context=dict)


# def donate_blood_view(request):
#     donation_form=forms.DonationForm()
#     if request.method=='POST':
#         donation_form=forms.DonationForm(request.POST)
#         if donation_form.is_valid():
#             blood_donate=donation_form.save(commit=False)
#             blood_donate.bloodgroup=donation_form.cleaned_data['bloodgroup']
#             donor= models.Donor.objects.get(user_id=request.user.id)
#             blood_donate.donor=donor
#             blood_donate.save()
#             return HttpResponseRedirect('donation-history')  
#     return render(request,'donor/donate_blood.html',{'donation_form':donation_form})
def donate_blood_view(request):
    # گرفتن اطلاعات اهداکننده از دیتابیس
    donor = models.Donor.objects.get(user_id=request.user.id)
    try:
        blood_donate = models.BloodDonate.objects.filter(donor=donor).latest('date')
        initial_data = {
            'bloodgroup': blood_donate.bloodgroup,
            'unit': blood_donate.unit,
            'disease': blood_donate.disease,
            'age': blood_donate.age,
        }
    except models.BloodDonate.DoesNotExist:
        initial_data = {
            'bloodgroup': donor.bloodgroup,
        }
    
    donation_form = forms.DonationForm(initial=initial_data)
    
    if request.method == 'POST':
        donation_form = forms.DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate = donation_form.save(commit=False)
            blood_donate.donor = donor
            blood_donate.save()
            return HttpResponseRedirect('donation-history')
    
    return render(request, 'donor/donate_blood.html', {'donation_form': donation_form})












def donation_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    donations=models.BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'donations':donations})


# def make_request_view(request):
#     donor = models.Donor.objects.get(user_id=request.user.id)  # دریافت اهداکننده
#     if request.method == 'POST':
#         request_form = bforms.RequestForm(request.POST)
#         if request_form.is_valid():
#             blood_request = request_form.save(commit=False)
#             blood_request.bloodgroup = request_form.cleaned_data['bloodgroup']
#             blood_request.request_by_donor = donor
#             blood_request.save()
#             return HttpResponseRedirect('request-history')
#     else:
#         request_form = bforms.RequestForm()

#     return render(request, 'donor/makerequest.html', {'request_form': request_form, 'donor': donor})



def make_request_view(request):
    try:
        donor = models.Donor.objects.get(user_id=request.user.id)
    except models.Donor.DoesNotExist:
        return HttpResponse("Donor not found", status=404)

    blood_request = models.BloodDonate.objects.first()
    if not blood_request:
        return HttpResponse("No BloodDonate record found", status=404)

    # مقداردهی اولیه به فرم
    initial_data = {
        'patient_name': f"{donor.user.first_name} {donor.user.last_name}",
        'patient_age': blood_request.age if blood_request.age else '',
        'reason': 'Nothing',
        'bloodgroup': donor.bloodgroup,  # مقداردهی اولیه گروپ خون
    }

    request_form = bforms.RequestForm(initial=initial_data)
    request_form.instance.bloodgroup = donor.bloodgroup  # مقداردهی instance فرم

    if request.method == 'POST':
        request_form = bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request = request_form.save(commit=False)
            blood_request.bloodgroup = request_form.cleaned_data.get('bloodgroup')
            blood_request.reason = request_form.cleaned_data.get('reason')
            blood_request.request_by_donor = donor
            blood_request.save()
            return HttpResponseRedirect('request-history')  # ریدایرکت به صفحه تاریخچه

    return render(request, 'donor/makerequest.html', {'request_form': request_form})






def request_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,'donor/request_history.html',{'blood_request':blood_request})
