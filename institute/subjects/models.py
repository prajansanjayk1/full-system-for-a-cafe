from django.db import models
from django.urls import reverse


class Subject(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='subjects/')

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('subjects:subject_detail', kwargs={'slug': self.slug})
