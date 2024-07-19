from django.shortcuts import render, redirect
from .forms import DoctorForm, PatientForm, ManagerForm
from .models import Doctor, Patient, Manager

def home(request):
    success_message = False
    error_message = None

    if request.method == 'POST':
        if 'doctor-submit' in request.POST:
            form = DoctorForm(request.POST)
            if form.is_valid():
                form.save()
                success_message = True
            else:
                error_message = form.errors
        elif 'patient-submit' in request.POST:
            form = PatientForm(request.POST)
            if form.is_valid():
                form.save()
                success_message = True
            else:
                error_message = form.errors
        elif 'manager-submit' in request.POST:
            form = ManagerForm(request.POST)
            if form.is_valid():
                form.save()
                success_message = True
            else:
                error_message = form.errors

        return render(request, 'hospital/home.html', {
            'doctor_form': DoctorForm(),
            'patient_form': PatientForm(),
            'manager_form': ManagerForm(),
            'success_message': success_message,
            'error_message': error_message,
        })

    return render(request, 'hospital/home.html', {
        'doctor_form': DoctorForm(),
        'patient_form': PatientForm(),
        'manager_form': ManagerForm(),
        'success_message': success_message,
        'error_message': error_message,
    })

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if user_type == 'doctor':
            user = Doctor.objects.filter(email=email, password=password).first()
        elif user_type == 'patient':
            user = Patient.objects.filter(email=email, password=password).first()
        elif user_type == 'manager':
            user = Manager.objects.filter(email=email, password=password).first()
        else:
            user = None

        if user:
            return redirect('dashboard')  # Başarıyla giriş yapıldığında dashboard sayfasına yönlendir
        else:
            return render(request, 'hospital/home.html', {
                'error_message': 'Giriş yapılamadı, lütfen kayıt oluşturunuz',
                'doctor_form': DoctorForm(),
                'patient_form': PatientForm(),
                'manager_form': ManagerForm(),
            })

    return redirect('home')  # GET isteği için ana sayfaya yönlendir

def dashboard(request):
    # Dashboard sayfası için gerekli verileri ve işlemleri buraya ekleyin
    return render(request, 'hospital/dashboard.html')
