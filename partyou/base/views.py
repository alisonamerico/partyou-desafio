# from django.contrib.auth import login, authenticate
# from django.contrib.auth.views import login as auth_login
from django.contrib import messages
from django.shortcuts import render
from .forms import ContactForm

from django.views.generic import (
    CreateView, TemplateView, UpdateView, FormView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm


from partyou.base.models import User
from .forms import UserCreationForm


class HomeView(TemplateView):

    template_name = 'base/home.html'


home = HomeView.as_view()


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'base/profile.html'


profile = ProfileView.as_view()


class LoginView(LoginRequiredMixin, TemplateView):

    template_name = 'base/home.html'


login = LoginView.as_view()


class RegisterView(CreateView):

    model = User
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


register = RegisterView.as_view()


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


# def register(request):
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
