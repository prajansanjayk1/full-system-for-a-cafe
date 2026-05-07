from django import forms
from .models import Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'student_name',
            'class_level',
            'subject_interest',
            'parent_name',
            'phone_number',
            'email',
            'message',
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError('Enter a valid phone number with at least 10 digits.')
        return phone

    def clean_student_name(self):
        name = self.cleaned_data['student_name'].strip()
        if len(name) < 2:
            raise forms.ValidationError('Student name is too short.')
        return name
