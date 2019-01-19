from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def contato(request):
    return render(request, 'base/contact.html')

