from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('courses/', include('courses.urls')),
    path('subjects/', include('subjects.urls')),
    path('results/', include('results.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
    path('registration/', include('registration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
