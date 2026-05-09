import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from mainapp.models import Lead

leads = Lead.objects.all()
total_leads = leads.count()
leads_with_email = leads.exclude(email__exact='').exclude(email__isnull=True).count()
leads_without_email = total_leads - leads_with_email

with open('leads_email_report.txt', 'w') as f:
    f.write(f"Total Leads: {total_leads}\n")
    f.write(f"Leads with Email: {leads_with_email}\n")
    f.write(f"Leads without Email: {leads_without_email}\n")
    if leads_without_email > 0:
        f.write("\nLeads missing email:\n")
        for lead in leads.filter(email__exact=''):
            f.write(f"- {lead.name} ({lead.phone})\n")
        for lead in leads.filter(email__isnull=True):
            f.write(f"- {lead.name} ({lead.phone})\n")

print("Report generated in leads_email_report.txt")
