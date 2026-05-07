from django.db import models


class Result(models.Model):
    student_name = models.CharField(max_length=150)
    subject = models.CharField(max_length=120)
    before_marks = models.PositiveIntegerField()
    after_marks = models.PositiveIntegerField()
    exam_name = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['-after_marks']

    def __str__(self) -> str:
        return f'{self.student_name} - {self.subject}'
