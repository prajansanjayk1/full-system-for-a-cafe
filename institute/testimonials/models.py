from django.db import models


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} ({self.role})'
