from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard URL'sini ekleyin
    
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    
    # Diğer URL desenleri...

    path('approve_appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('reject_appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),

]
