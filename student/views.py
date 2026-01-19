from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
# Create your views here.

def students(request):
    
    student = [ {
        "id":1,
        "name": "Jhon doe",
        "age":26
    }
    ]
    
    return HttpResponse(student)