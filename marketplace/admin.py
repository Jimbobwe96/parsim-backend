from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Listing)

admin.site.register(models.ListingImage)

admin.site.register(models.Category)

admin.site.register(models.Message)

admin.site.register(models.Review)

admin.site.register(models.Notification)