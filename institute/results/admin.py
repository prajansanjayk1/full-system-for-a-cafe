from django.contrib import admin
from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'subject', 'before_marks', 'after_marks')
    search_fields = ('student_name', 'subject')
