from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ContactForm, RegisterForm

from django.views.generic import (
    TemplateView, UpdateView, FormView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class HomeView(TemplateView):

    template_name = 'base/home.html'


home = HomeView.as_view()


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'base/profile.html'


profile = ProfileView.as_view()


class LoginView(LoginRequiredMixin, TemplateView):

    template_name = 'base/home.html'


login = LoginView.as_view()


class UpdateUserView(LoginRequiredMixin, UpdateView):

    model = User
    template_name = 'base/update_user.html'
    fields = ['first_name', 'email']
    success_url = reverse_lazy('base:profile')

    def get_object(self):
        return self.request.user


update_user = UpdateUserView.as_view()


class UpdatePasswordView(LoginRequiredMixin, FormView):

    model = User
    template_name = 'base/update_password.html'
    success_url = reverse_lazy('base:profile')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


update_password = UpdatePasswordView.as_view()


def register(request):
    if request.method == 'POST':  # pragma: no cover
        form = RegisterForm(request.POST)  # pragma: no cover
        if form.is_valid():  # pragma: no cover
            form.save()  # pragma: no cover
            username = form.cleaned_data.get('username')  # pragma: no cover
            raw_password = form.cleaned_data.get('password1')  # pragma: no cover
            user = authenticate(username=username, password=raw_password)  # pragma: no cover
            login(request, user)  # pragma: no cover
            return redirect('base:home')  # pragma: no cover
    else:
        form = RegisterForm()  # pragma: no cover
    return render(request, 'base/register.html', {'form': form})  # pragma: no cover


def contact(request):
    success = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_email()
        success = True
    elif request.method == 'POST':
        messages.error(request, 'Formulário Inválido')
    context = {
        'form': form,
        'success': success
    }
    return render(request, 'base/contact.html', context)
