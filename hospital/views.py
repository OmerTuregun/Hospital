from django.shortcuts import render, redirect
from .forms import DoctorForm, PatientForm, ManagerForm, AppointmentForm
from .models import Doctor, Patient, Manager, Appointment

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
            if user:
                request.session['user_name'] = user.first_name
                request.session['user_surname'] = user.last_name
                request.session['user_email'] = email
                request.session['user_hospital'] = user.hospital
                request.session['user_specialization'] = user.specialization
                return redirect('doctor_dashboard')
        elif user_type == 'patient':
            user = Patient.objects.filter(email=email, password=password).first()
            if user:
                request.session['user_name'] = user.first_name
                request.session['user_surname'] = user.last_name
                request.session['user_email'] = email
                request.session['user_phone'] = user.phone
                # Convert date object to string
                request.session['user_dob'] = user.dob.strftime('%Y-%m-%d')
                return redirect('patient_dashboard')
        elif user_type == 'manager':
            user = Manager.objects.filter(email=email, password=password).first()
            if user:
                request.session['user_name'] = user.first_name
                request.session['user_surname'] = user.last_name
                request.session['user_email'] = email
                return redirect('manager_dashboard')
        else:
            user = None

        return render(request, 'hospital/home.html', {
            'error_message': 'Giriş yapılamadı, lütfen kayıt oluşturunuz',
            'doctor_form': DoctorForm(),
            'patient_form': PatientForm(),
            'manager_form': ManagerForm(),
        })

    return redirect('home')

def dashboard(request):
    return render(request, 'hospital/dashboard.html')

def manager_dashboard(request):
    user_name = request.session.get('user_name', 'Yönetici')
    user_surname = request.session.get('user_surname', '')
    user_email = request.session.get('user_email', '')

    context = {
        'user_name': user_name,
        'user_surname': user_surname,
        'user_email': user_email,
    }

    return render(request, 'hospital/manager_dashboard.html', context)

def patient_dashboard(request):
    user_name = request.session.get('user_name', 'Hasta')
    user_surname = request.session.get('user_surname', '')
    user_email = request.session.get('user_email', '')
    user_phone = request.session.get('user_phone', '')
    user_dob = request.session.get('user_dob', '')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = Patient.objects.get(email=user_email)
            appointment.status = 'Pending'  # Set the status to Pending for approval
            appointment.save()
            # Add notification here
            return redirect('patient_dashboard')  # Başarıyla yönlendirin
    else:
        form = AppointmentForm()

    context = {
        'user_name': user_name,
        'user_surname': user_surname,
        'user_email': user_email,
        'user_phone': user_phone,
        'user_dob': user_dob,
        'appointment_form': form,
    }
    return render(request, 'hospital/patient_dashboard.html', context)

def doctor_dashboard(request):
    user_name = request.session.get('user_name', 'Doktor')
    user_surname = request.session.get('user_surname', '')
    user_email = request.session.get('user_email', '')
    user_hospital = request.session.get('user_hospital', '')
    user_specialization = request.session.get('user_specialization', '')

    # Get pending appointments for notification
    pending_appointments = Appointment.objects.filter(doctor__email=user_email, status='Pending')

    # Get approved appointments
    approved_appointments = Appointment.objects.filter(doctor__email=user_email, status='Approved').order_by('date', 'time')

    context = {
        'user_name': user_name,
        'user_surname': user_surname,
        'user_email': user_email,
        'user_hospital': user_hospital,
        'user_specialization': user_specialization,
        'approved_appointments': approved_appointments,  # Approved appointments
        'pending_appointments': pending_appointments,  # Pending appointments for notification
    }
    return render(request, 'hospital/doctor_dashboard.html', context)

def approve_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = 'Approved'
    appointment.save()
    return redirect('doctor_dashboard')

def reject_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect('doctor_dashboard')
