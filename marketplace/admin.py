from django.contrib import admin
from . import models

@admin.register(models.Listing)
class ListingAdmin(admin.ModelAdmin):
  list_display = [field.name for field in models.Listing._meta.fields]

  # Exclude some fields from being edited
  list_editable = [field.name for field in models.Listing._meta.fields 
                   if field.name not in ['id', 'date_posted', 'seller']]
  list_per_page = 20


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
  list_display = [field.name for field in models.User._meta.fields]

  # Exclude some fields from being edited
  list_editable = [field.name for field in models.User._meta.fields 
                   if field.name not in ['id', 'password', 'date_joined']]
  list_per_page = 20

admin.site.register(models.ListingImage)

admin.site.register(models.Category)

admin.site.register(models.Message)

admin.site.register(models.Review)

admin.site.register(models.Notification)