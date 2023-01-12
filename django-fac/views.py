from django.shortcuts import render, HttpResponse

# Create your views here.
def health(request):
    return HttpResponse("OK")
