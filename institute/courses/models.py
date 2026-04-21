from django.db import models
from django.urls import reverse


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    class_level = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})
