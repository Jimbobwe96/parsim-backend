from django.contrib import admin
from django.urls import path, include
from . import views

admin.site.site_header = 'Parsim Admin'
admin.site.index_title = 'Admin Dashboard'

# UrlConf
urlpatterns = [
    path('admin/', admin.site.urls),
    path('listings/', views.view_listings),
]