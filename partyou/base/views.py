from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from partyou.base.forms import RegisterForm
from partyou.produtos.models import Category, Product


def home(request):
    categories = Category.objects.all()
    produtos = Product.objects.all()
    context = {'categories': categories,
               'produtos': produtos,}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')


def contato(request):
    return render(request, 'base/contact_detail.html')


def registro(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'base/register.html', {'form': form})
