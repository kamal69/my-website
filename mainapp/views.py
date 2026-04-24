import csv
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Lead, Property, SiteVisit

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('dashboard')
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
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    return render(request, 'register.html')

@login_required
def dashboard_view(request):
    if not request.user.is_staff:
        return redirect('index')
    
    leads = Lead.objects.all()[:10]
    stats = {
        'total_properties': Property.objects.count(),
        'active_leads': Lead.objects.count(),
        'deals_closed': 42, # Placeholder or can be dynamic if we add status to Lead
        'revenue': "4.2 Cr" # Placeholder
    }
    context = {
        'leads': leads,
        'stats': stats
    }
    return render(request, 'dashboard.html', context)

def admin_login_view(request):
    return render(request, 'admin_login.html')

@login_required
def profile_view(request):
    user_leads = Lead.objects.filter(user=request.user).order_by('-submitted_at')
    
    # Get latest phone number from inquiries
    latest_lead = user_leads.first()
    latest_phone = latest_lead.phone if latest_lead else "Not provided"
    
    context = {
        'leads': user_leads,
        'inquiry_count': user_leads.count(),
        'latest_phone': latest_phone
    }
    return render(request, 'profile.html', context)

@login_required
def update_lead_phone_view(request, lead_id):
    try:
        lead = Lead.objects.get(id=lead_id, user=request.user)
    except Lead.DoesNotExist:
        messages.error(request, "Lead not found or you don't have permission to edit it.")
        return redirect('profile')

    if request.method == 'POST':
        new_phone = request.POST.get('phone', '').strip()
        if new_phone:
            lead.phone = new_phone
            lead.save()
            messages.success(request, 'Mobile number updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Mobile number cannot be empty.')
            
    return render(request, 'update_phone.html', {'lead': lead})

def leads_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        property_interest = request.POST.get('property_interest', 'flat')
        preferred_location = request.POST.get('preferred_location', 'mohali')
        budget = request.POST.get('budget', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and phone and email:
            otp = str(random.randint(1000, 9999))
            request.session['lead_data'] = {
                'name': name,
                'phone': phone,
                'email': email,
                'property_interest': property_interest,
                'preferred_location': preferred_location,
                'budget': budget,
                'message': message_text,
            }
            request.session['lead_otp'] = otp
            
            # Send OTP via email
            from django.conf import settings
            subject = 'Your Verification OTP - RKG Sovereign Realty'
            message = f'Hello {name},\n\nYour OTP for verifying your lead inquiry is: {otp}\n\nThank you,\nRKG Sovereign Realty'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            
            messages.info(request, 'An OTP has been sent to your email. Please enter it to verify your inquiry.')
            return redirect('verify_otp')
        else:
            messages.error(request, 'Please provide your name, phone number, and email.')
    return render(request, 'leads.html')

def verify_otp_view(request):
    if 'lead_data' not in request.session or 'lead_otp' not in request.session:
        messages.error(request, 'Session expired. Please submit your inquiry again.')
        return redirect('leads')
        
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        if entered_otp == request.session['lead_otp']:
            lead_data = request.session['lead_data']
            lead = Lead.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=lead_data['name'],
                phone=lead_data['phone'],
                email=lead_data['email'],
                property_interest=lead_data['property_interest'],
                preferred_location=lead_data['preferred_location'],
                budget=lead_data['budget'] if lead_data['budget'] else None,
                message=lead_data['message'] if lead_data['message'] else None,
            )
            del request.session['lead_data']
            del request.session['lead_otp']

            # Send Emails (Both Client and Admin)
            from django.conf import settings
            
            # 1. Welcome/Confirmation Email to Client
            client_subject = 'Inquiry Received - RKG Sovereign Realty'
            client_message = f'''Dear {lead.name},

Thank you for your interest in RKG Sovereign Realty. Your inquiry has been successfully verified.

Summary of your inquiry:
- Property Type: {lead.get_property_interest_display()}
- Preferred Location: {lead.get_preferred_location_display()}
- Budget: {lead.budget if lead.budget else 'Not specified'}
- Your Message: {lead.message if lead.message else 'None'}

Our team will contact you shortly on your provided number: {lead.phone}

Thank you,
RKG Sovereign Realty'''
            send_mail(client_subject, client_message, settings.DEFAULT_FROM_EMAIL, [lead.email])

            # 2. Notification Email to Admin
            admin_subject = 'NEW LEAD RECEIVED - RKG Website'
            admin_message = f'''Hello Admin,

A new verified lead has been submitted:

Name: {lead.name}
Phone: {lead.phone}
Email: {lead.email}
Interest: {lead.get_property_interest_display()}
Location: {lead.get_preferred_location_display()}
Budget: {lead.budget if lead.budget else 'N/A'}
Message: {lead.message if lead.message else 'N/A'}

Check the Admin Dashboard for details.'''
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.EMAIL_HOST_USER])

            messages.success(request, 'Thank you! Your inquiry has been verified and submitted successfully. We will contact you shortly.')
            return redirect('leads')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            
    return render(request, 'verify_otp.html')

@login_required
def request_correct_number_view(request, lead_id):
    if not request.user.is_staff:
        return redirect('index')
        
    try:
        lead = Lead.objects.get(id=lead_id)
        if lead.email:
            from django.conf import settings
            subject = 'Action Required: Update Your Mobile Number - RKG Sovereign Realty'
            message = f'''Dear {lead.name},

We received your property inquiry but noticed that the mobile number provided ({lead.phone}) seems to be unreachable or incorrect.

To help us connect with you properly and provide our best service, kindly reply to this email with your correct and active mobile number.

Thank you,
RKG Sovereign Realty Team'''
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [lead.email])
            messages.success(request, f'Correction request email sent to {lead.email}.')
        else:
            messages.error(request, 'This lead does not have an email address.')
    except Lead.DoesNotExist:
        messages.error(request, 'Lead not found.')
        
    return redirect('dashboard')

@login_required
def add_property_view(request):
    if not request.user.is_staff:
        return redirect('index')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        price = request.POST.get('price')
        property_type = request.POST.get('property_type')
        
        Property.objects.create(
            title=title,
            description=description,
            location=location,
            price=price,
            property_type=property_type
        )
        messages.success(request, 'Property added successfully!')
        return redirect('dashboard')
    
    context = {
        'property_choices': Lead.PROPERTY_CHOICES
    }
    return render(request, 'add_property.html', context)

@login_required
def schedule_visit_view(request):
    if not request.user.is_staff:
        return redirect('index')
    
    if request.method == 'POST':
        lead_id = request.POST.get('lead')
        property_id = request.POST.get('property')
        visit_date = request.POST.get('visit_date')
        visit_time = request.POST.get('visit_time')
        notes = request.POST.get('notes')
        
        SiteVisit.objects.create(
            lead_id=lead_id,
            property_id=property_id,
            visit_date=visit_date,
            visit_time=visit_time,
            notes=notes
        )
        messages.success(request, 'Site visit scheduled!')
        return redirect('dashboard')
    
    context = {
        'leads': Lead.objects.all(),
        'properties': Property.objects.all()
    }
    return render(request, 'schedule_visit.html', context)

@login_required
def export_leads_view(request):
    if not request.user.is_staff:
        return redirect('index')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rkg_leads_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Email', 'Interest', 'Location', 'Budget', 'Date'])
    
    leads = Lead.objects.all().values_list('name', 'phone', 'email', 'property_interest', 'preferred_location', 'budget', 'submitted_at')
    for lead in leads:
        writer.writerow(lead)
        
    return response

@login_required
def delete_lead_view(request, lead_id):
    if not request.user.is_staff:
        return redirect('index')
    
    try:
        lead = Lead.objects.get(id=lead_id)
        lead.delete()
        messages.success(request, 'Lead deleted successfully.')
    except Lead.DoesNotExist:
        messages.error(request, 'Lead not found.')
        
    return redirect('dashboard')

@login_required
def edit_lead_view(request, lead_id):
    if not request.user.is_staff:
        return redirect('index')
    
    try:
        lead = Lead.objects.get(id=lead_id)
    except Lead.DoesNotExist:
        messages.error(request, 'Lead not found.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        lead.name = request.POST.get('name')
        lead.phone = request.POST.get('phone')
        lead.email = request.POST.get('email')
        lead.property_interest = request.POST.get('property_interest')
        lead.preferred_location = request.POST.get('preferred_location')
        lead.budget = request.POST.get('budget')
        lead.message = request.POST.get('message')
        lead.save()
        messages.success(request, 'Lead updated successfully!')
        return redirect('dashboard')
    
    context = {
        'lead': lead,
        'property_choices': Lead.PROPERTY_CHOICES,
        'location_choices': Lead.LOCATION_CHOICES
    }
    return render(request, 'edit_lead.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')
