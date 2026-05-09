import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from mainapp.models import Property

properties = [
    {"title": "Luxury Flat", "location": "Chandigarh", "price": "1.2 Cr", "property_type": "flat", "description": "Premium flat in Chandigarh."},
    {"title": "3BHK Apartment", "location": "Mohali", "price": "75 L", "property_type": "flat", "description": "Spacious apartment in Mohali."},
    {"title": "Residential Plot", "location": "Zirakpur", "price": "45 L", "property_type": "plot", "description": "Prime plot in Zirakpur."},
    {"title": "Premium Villa", "location": "Panchkula", "price": "2.5 Cr", "property_type": "villa", "description": "Luxury villa in Panchkula."},
    {"title": "Modern Studio", "location": "Kharar", "price": "25 L", "property_type": "room", "description": "Cozy studio in Kharar."},
    {"title": "Commercial Shop", "location": "Airport Road", "price": "1 Cr", "property_type": "commercial", "description": "High visibility shop."},
    {"title": "Agricultural Land", "location": "Haryana", "price": "2 Cr", "property_type": "farm", "description": "Large farm land."},
    {"title": "Studio PG", "location": "Chandigarh", "price": "15 L", "property_type": "room", "description": "Student friendly PG."},
    {"title": "Industrial Complex", "location": "Mohali", "price": "5 Cr", "property_type": "building", "description": "Large building for industry."},
]

for p in properties:
    Property.objects.get_or_create(
        title=p["title"],
        location=p["location"],
        price=p["price"],
        property_type=p["property_type"],
        defaults={"description": p["description"]}
    )

print("Successfully added sample properties to the database.")
