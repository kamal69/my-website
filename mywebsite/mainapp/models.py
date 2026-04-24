from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    PROPERTY_CHOICES = [
        ('residential', 'Residential Villas'),
        ('apartments', 'Luxury Apartments'),
        ('commercial', 'Commercial Space'),
        ('plot', 'Empty Plots'),
    ]

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    property_interest = models.CharField(max_length=50, choices=PROPERTY_CHOICES, default='residential')
    message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone} ({self.submitted_at.strftime('%d %b %Y')})"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
