import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from mainapp.models import Dealer

dealers = [
    {"name": "Mann Sharma estate", "phone": "9815801444, 8699008181"},
    {"name": "Manav estate", "phone": "9872425055, 7973158658"},
    {"name": "Mohali Estate", "phone": "9988206114"},
    {"name": "Deep Associate", "phone": "9999466665, 9811163770"},
    {"name": "Chaudhary property consultant", "phone": "709709661, 7097096663"},
    {"name": "Narender GBP", "phone": "9816798343"},
]

for d in dealers:
    Dealer.objects.get_or_create(name=d["name"], defaults={"phone": d["phone"]})

print("Successfully added initial dealers to the database.")
