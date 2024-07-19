from django import forms
from .models import Doctor, Patient, Manager
import datetime

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'hospital', 'specialization', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Doctor.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi ile zaten bir doktor kaydı mevcut.")
        return email

class PatientForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Geçerli bir tarih girin."
    )
    
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone', 'dob', 'password']
    
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob and dob > datetime.date.today():
            raise forms.ValidationError("Doğum tarihi gelecekte olamaz.")
        return dob

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Patient.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi ile zaten bir hasta kaydı mevcut.")
        return email

class ManagerForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'type': 'email'}),
        help_text="Geçerli bir e-posta girin."
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'type': 'password'}),
        help_text="Şifre en az 6 karakter uzunluğunda olmalıdır."
    )

    class Meta:
        model = Manager
        fields = ['first_name', 'last_name', 'email', 'password']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Manager.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi ile zaten bir yönetici kaydı mevcut.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Şifre en az 6 karakter uzunluğunda olmalıdır.")
        return password
