from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'class_level', 'subject_interest', 'phone_number', 'submitted_at')
    search_fields = ('student_name', 'subject_interest', 'parent_name', 'phone_number')
    readonly_fields = ('submitted_at',)
