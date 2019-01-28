# from django.contrib.auth import login, authenticate

from django.shortcuts import render
from .forms import ContactForm


def home(request):
    return render(request, 'base/home.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
    else:
        form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'base/contact.html', context)


# def registro(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = RegisterForm()
#     return render(request, 'base/register.html', {'form': form})
