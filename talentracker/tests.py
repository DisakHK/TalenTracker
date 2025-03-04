from django.test import TestCase
from django.http import HttpResponse
# Create your tests here.

def home(request):
    return HttpResponse('<h1>Home Page</h1>')