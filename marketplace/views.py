from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request handler pretty much

def view_listings(request):
    return HttpResponse('hello world')