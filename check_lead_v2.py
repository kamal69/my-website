import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from mainapp.models import Lead

lead = Lead.objects.filter(name__icontains='Kamal Jeet').first()
with open('lead_result.txt', 'w') as f:
    if lead:
        f.write(f"Lead Name: {lead.name}\n")
        f.write(f"Lead Email: {lead.email}\n")
    else:
        f.write("Lead 'Kamal Jeet' not found.\n")
