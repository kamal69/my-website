import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from mainapp.models import Property

count = Property.objects.count()
print(f"Total Properties in Database: {count}")

if count == 0:
    print("Database is empty. Adding some sample properties...")
    Property.objects.create(title="Skyline Penthouse", location="Sector 66, Mohali", price="1.2 Cr", property_type="flat", description="Luxury penthouse with view.")
    Property.objects.create(title="Omaxe Villas", location="Aerocity", price="85 L", property_type="villa", description="Premium 3BHK villa.")
    Property.objects.create(title="Commercial Shop", location="Airport Road", price="45 L", property_type="commercial", description="Busy market location.")
    print("Sample properties added.")
