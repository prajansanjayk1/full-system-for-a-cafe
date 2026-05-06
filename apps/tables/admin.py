from django.contrib import admin

from . import models

for name in dir(models):
    model = getattr(models, name)
    if getattr(model, "_meta", None) and not model._meta.abstract:
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass
