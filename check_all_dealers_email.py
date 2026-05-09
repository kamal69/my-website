import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from mainapp.models import Dealer

dealers = Dealer.objects.all()
total_dealers = dealers.count()
dealers_with_email = dealers.exclude(email__exact='').exclude(email__isnull=True).count()
dealers_without_email = total_dealers - dealers_with_email

with open('dealers_email_report.txt', 'w') as f:
    f.write(f"Total Dealers: {total_dealers}\n")
    f.write(f"Dealers with Email: {dealers_with_email}\n")
    f.write(f"Dealers without Email: {dealers_without_email}\n")
    if dealers_without_email > 0:
        f.write("\nDealers missing email:\n")
        for d in dealers.filter(email__exact=''):
            f.write(f"- {d.name} ({d.phone})\n")
        for d in dealers.filter(email__isnull=True):
            f.write(f"- {d.name} ({d.phone})\n")

print("Report generated in dealers_email_report.txt")
