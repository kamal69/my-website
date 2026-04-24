from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('profile/', views.profile_view, name='profile'),
    path('leads/', views.leads_view, name='leads'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('add-property/', views.add_property_view, name='add_property'),
    path('schedule-visit/', views.schedule_visit_view, name='schedule_visit'),
    path('export-leads/', views.export_leads_view, name='export_leads'),
    path('delete-lead/<int:lead_id>/', views.delete_lead_view, name='delete_lead'),
    path('edit-lead/<int:lead_id>/', views.edit_lead_view, name='edit_lead'),
    path('request-correct-number/<int:lead_id>/', views.request_correct_number_view, name='request_correct_number'),
    path('update-phone/<int:lead_id>/', views.update_lead_phone_view, name='update_phone'),
]
