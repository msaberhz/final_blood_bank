from django.urls import path

from django.contrib.auth.views import LoginView
from . import views
from .views import update_patient
urlpatterns = [
    path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html'),name='patientlogin'),
    path('patientsignup', views.patient_signup_view,name='patientsignup'),
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('make-request', views.make_request_view,name='make-request'),
    path('my-request', views.my_request_view,name='my-request'),
    path('p_feedback', views.p_feedback_view, name='p_feedback'),
    path('update/', update_patient, name='update_patient'),
]