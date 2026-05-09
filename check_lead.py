import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from mainapp.models import Lead

lead = Lead.objects.filter(name__icontains='Kamal Jeet').first()
if lead:
    print(f"Lead Name: {lead.name}")
    print(f"Lead Email: {lead.email}")
else:
    print("Lead 'Kamal Jeet' not found.")
