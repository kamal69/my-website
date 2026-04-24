from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'property_interest', 'submitted_at')
    list_filter = ('property_interest', 'submitted_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
