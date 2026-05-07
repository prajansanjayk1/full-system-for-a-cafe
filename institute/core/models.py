from django.db import models


class SiteSettings(models.Model):
    institute_name = models.CharField(max_length=200, default='SD Institute')
    tagline = models.CharField(max_length=255, blank=True)
    about_content = models.TextField()
    why_choose_us = models.TextField(help_text='One point per line.')
    hero_heading = models.CharField(max_length=255)
    hero_subheading = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    class Meta:
        verbose_name_plural = 'Site Settings'

    def __str__(self) -> str:
        return self.institute_name
