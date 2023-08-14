from django.http import HttpResponse
from .view_modules.auth.registration.RegistrationForm import RegistrationForm
from .view_modules.auth.login.LogInForm import LogInForm

def register(request):
    registration_form = RegistrationForm()  
    return registration_form.post(request)  

def log_in(request):
    sign_in_form = LogInForm()  
    return sign_in_form.post(request)  
