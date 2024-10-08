from django.urls import path
from . import views

# UrlConf
urlpatterns = [
    path('listings/', views.view_listings),
]