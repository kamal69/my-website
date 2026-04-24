from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'property_interest', 'preferred_location', 'budget', 'submitted_at')
    list_filter = ('property_interest', 'preferred_location', 'submitted_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
    list_per_page = 50
