from django.db import models


class Registration(models.Model):
    CLASS_CHOICES = [
        ('9', 'Class 9'),
        ('10', 'Class 10'),
        ('11', 'Class 11'),
        ('12', 'Class 12'),
    ]

    student_name = models.CharField(max_length=150)
    class_level = models.CharField(max_length=2, choices=CLASS_CHOICES)
    subject_interest = models.CharField(max_length=150)
    parent_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self) -> str:
        return f'{self.student_name} ({self.class_level})'
