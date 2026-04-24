from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    PROPERTY_CHOICES = [
        ('flat', 'Flat / Apartment'),
        ('room', 'Room / PG / Studio'),
        ('plot', 'Residential Plot'),
        ('villa', 'Independent Villa / House'),
        ('commercial', 'Commercial Space / Shop / Office'),
        ('building', 'Building / Complex'),
        ('farm', 'Farm House / Agricultural Land'),
        ('other', 'Other'),
    ]
    LOCATION_CHOICES = [
        ('chandigarh', 'Chandigarh'),
        ('mohali', 'Mohali'),
        ('zirakpur', 'Zirakpur'),
        ('panchkula', 'Panchkula'),
        ('kharar', 'Kharar'),
        ('haryana', 'Haryana (Other)'),
        ('other', 'Other Location'),
    ]

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    property_interest = models.CharField(max_length=50, choices=PROPERTY_CHOICES, default='flat')
    preferred_location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='mohali')
    budget = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone} ({self.submitted_at.strftime('%d %b %Y')})"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50, choices=Lead.PROPERTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

class SiteVisit(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    visit_date = models.DateField()
    visit_time = models.TimeField()
    status = models.CharField(max_length=50, default='scheduled', choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit for {self.lead.name} at {self.property.title} on {self.visit_date}"
