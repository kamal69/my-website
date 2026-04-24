from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lead

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Django auth usually requires username. We'll find user by email.
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('fullname', '')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')

    return render(request, 'register.html')

@login_required
def dashboard_view(request):
    return redirect('index')

def admin_login_view(request):
    return render(request, 'admin_login.html')

@login_required
def profile_view(request):
    user_leads = Lead.objects.filter(user=request.user).order_by('-submitted_at')
    context = {
        'leads': user_leads,
    }
    return render(request, 'profile.html', context)

@login_required
def leads_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        property_interest = request.POST.get('property_interest', 'residential')
        message_text = request.POST.get('message', '').strip()

        if name and phone:
            Lead.objects.create(
                user=request.user,
                name=name,
                phone=phone,
                email=email if email else None,
                property_interest=property_interest,
                message=message_text if message_text else None,
            )
            messages.success(request, 'Thank you! Your inquiry has been submitted. We will contact you within 24 hours.')
            return redirect('leads')
        else:
            messages.error(request, 'Please provide both your name and phone number.')

    return render(request, 'leads.html')

def logout_view(request):
    logout(request)
    return redirect('index')
